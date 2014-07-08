from django import forms
from django.template import Context, Template, TemplateSyntaxError
from django.test import SimpleTestCase
from unittest import TestCase


class TestForm(forms.Form):
    """
    Dummy form for testing purposes.

    """
    name = forms.CharField(label="Name")
    is_cool = forms.BooleanField(label='is cool?')
    gender = forms.ChoiceField(
        label="Gender",
        widget=forms.RadioSelect()
    )


class SelectForm(forms.Form):
    """
    Form with a choice field.

    """
    CHOICES = [
        (1, 'One'),
        (2, 'Two'),
    ]
    model = forms.TypedChoiceField(choices=CHOICES)
    radio = forms.TypedChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    multiple = forms.TypedMultipleChoiceField(choices=CHOICES)


class TemplateTestMixin(object):
    TEMPLATE_BASE = """{{% load formulation %}}{{% form 'test.form' %}}{0}{{% endform %}}"""

    @classmethod
    def setUpClass(cls):
        cls.context = Context({'form': TestForm()})

    def _render_string(self, template, context=None):
        t = Template(self.TEMPLATE_BASE.format(template))
        if context is None:
            context = Context()
        return t.render(context)


class FieldTagTest(TemplateTestMixin, SimpleTestCase):
    """
    Testing template tags.

    """
    def test_use_correct_block(self):
        """
        Make sure the field tag uses the right block specified.

        """
        template = """{% field form.name 'custom_input' %}"""
        self.assertEqual(
            self._render_string(template, self.context),
            """<input type="text" name="name" value="">"""
        )

    def test_unknown_block(self):
        """
        Trying to render a block that doesn't exist raises an error.

        """
        template = """{% field form.name 'does_not_exist' %}"""
        with self.assertRaises(TemplateSyntaxError):
            self._render_string(template, self.context)

    def test_auto_widget(self):
        """
        Choose the correct widget according to the form field.

        """
        template = """{% field form.name %}"""
        self.assertEqual(
            self._render_string(template, self.context),
            """auto widget CharField_TextInput_name"""
        )

        template = """{% field form.gender %}"""
        self.assertEqual(
            self._render_string(template, self.context),
            """auto widget ChoiceField_RadioSelect"""
        )

        template = """{% field form.is_cool %}"""
        self.assertEqual(
            self._render_string(template, self.context),
            """auto widget CheckboxInput"""
        )

    def test_force_text_widgets(self):
        """
        Model choice fields use int(value)s which will not evaluate to True
        when compared to a str(value) of the widget.
        This test is to make sure that previously selected fields
        or initial data are selected correctly.

        The value of the widget is also normalized, test the widgets where this
        applies.

        """
        # Test the select widget
        initial1 = {
            'model': 2,
            'radio': 1,
            'multiple': [1, 2]
        }
        initial2 = {
            'model': '2',
            'radio': '1',
            'multiple': ['1', '2']
        }
        ctx1 = Context({'form': SelectForm(initial=initial1)})
        ctx2 = Context({'form': SelectForm(initial=initial2)})

        template = """{% field form.model %}"""
        expected_html = """<option value="2" selected>Two</option>"""
        self.assertInHTML(expected_html, self._render_string(template, ctx1))
        self.assertInHTML(expected_html, self._render_string(template, ctx2))

        # Test radio's
        template = """{% field form.radio %}"""
        expected_html = """<label><input type="radio" id="id_radio_0" value="1" checked>One</label>"""
        self.assertInHTML(expected_html, self._render_string(template, ctx1))
        self.assertInHTML(expected_html, self._render_string(template, ctx2))

        # Test multiple
        template = """{% field form.multiple %}"""
        expected_html1 = """<option value="1" selected>One</option>"""
        expected_html2 = """<option value="2" selected>Two</option>"""
        self.assertInHTML(expected_html1, self._render_string(template, ctx1))
        self.assertInHTML(expected_html2, self._render_string(template, ctx1))
        self.assertInHTML(expected_html1, self._render_string(template, ctx2))
        self.assertInHTML(expected_html2, self._render_string(template, ctx2))


class UseTagTest(TemplateTestMixin, TestCase):
    """
    Tests for the {% use %} tag.

    """
    def test_use_tag(self):
        """
        Basic use tag usage.

        """
        template = """{% use 'use_test' test='use tag test' %}"""
        self.assertEqual(
            self._render_string(template),
            """use tag test"""
        )

    def test_use_tag_inherits_context(self):
        """
        Use tag should inherit context.

        """
        template = """{% use 'use_test_context' %}"""
        context = Context({'test': 'use tag test'})
        self.assertEqual(
            self._render_string(template, context),
            """use tag test"""
        )


class FlatAttrsFilterTest(TemplateTestMixin, TestCase):
    """
    Make sure our flatattrs filter works.

    """
    def test_flat_attrs_filter(self):
        """
        Flat attrs filter does what it's supposed to do.

        NOTE: Attributes are sorted alphabetically.

        """
        template = """<input{{ attrs|flat_attrs }}>"""
        context = Context({'attrs': {
            'name': 'test',
            'id': 'id_test',
        }})
        self.assertEqual(
            self._render_string(template, context),
            """<input id="id_test" name="test">"""
        )


class DefaultTemplateTest(TestCase):
    """
    Test the provided default template(s).

    TODO make the tests go through all default widgets.

    """
    template = """
        {{% load formulation %}}
        {{% form '{0}' %}}
        {{% field form.name %}}
        {{% field form.is_cool %}}
        {{% endform %}}
    """

    def _render_string(self, template, context=None):
        t = Template(template)
        if context is None:
            context = Context({'form': TestForm()})
        return t.render(context)

    def test_default_template(self):
        """
        Testing default.form template.

        """
        template = self.template.format('formulation/default.form')
        try:
            render = self._render_string(template)
        except TemplateSyntaxError:
            self.fail('Default template throws syntax error.')


class InheritanceTest(TemplateTestMixin, TestCase):
    """ Test that extending and block inheritance work correctly """
    TEMPLATE_BASE = """{{% load formulation %}}{{% form 'test2.form' %}}{0}{{% endform %}}"""

    def test_inherited_form(self):
        template = """{% field form.name 'Inherited' %}"""
        self.assertEqual(
            self._render_string(template, self.context),
            """foobar"""
        )
