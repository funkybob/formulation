from django import forms
from django.template import Context, Template, TemplateSyntaxError
from django.template.loader import get_template
from django.test import SimpleTestCase
from django.test.utils import setup_test_template_loader, restore_template_loaders


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
    TEMPLATE_BASE = '''{{% load formulation %}}{{% form 'test.form' %}}{}{{% endform %}}'''
    TEMPLATES = {}
    PARTIALS = {}

    @classmethod
    def setUpClass(cls):
        cls.context = Context({'form': TestForm()})
        for key, tmpl in cls.PARTIALS.items():
            cls.TEMPLATES[key] = cls.TEMPLATE_BASE.format(tmpl)
        setup_test_template_loader(cls.TEMPLATES)

    @classmethod
    def tearDownClass(cls):
        restore_template_loaders()

STOCK_TEMPLATE = '''{{% load formulation %}}{{% form 'test.form' %}}{}{{% endform %}}'''

class FieldTagTest(TemplateTestMixin, SimpleTestCase):
    """
    Testing template tags.
    """

    TEMPLATES = {
        'test.form': '''
{% load formulation %}
{% block input %}<input type="{{ field_type }}" name="{{ html_name }}" value="{{ value|default:"" }}">{% endblock %}
{% block custom_input %}{% use 'input' field_type="text" %}{% endblock %}

{% block CharField_TextInput_name %}auto widget CharField_TextInput_name{% endblock %}
{% block ChoiceField_RadioSelect %}auto widget ChoiceField_RadioSelect{% endblock %}
{% block CheckboxInput %}auto widget CheckboxInput{% endblock %}

{% block use_test %}{{ test }}{% endblock %}
{% block use_test_context %}{{ test }}{% endblock %}

Tests for proper selected value detection.
{% block Select %}
<select name="{{ html_name }}">
{% for val, display in choices %}
  <option value="{{ val }}" {% if val == value|default:'' %}selected{% endif %}>{{ display }}</option>
{% endfor %}
</select>
{% endblock %}

{% block SelectMultiple %}
<select name="{{ html_name }}" multiple>
{% for val, display in choices %}
    <option value="{{ val }}" {% if val in value %}selected{% endif %}>{{ display }}</option>
{% endfor %}
</select>
{% endblock %}

{% block RadioSelect %}
<ul id="{{ id }}">
{% for val, display in choices %}
    <li><label><input type="radio" id="{{ id}}_{{ forloop.counter0 }}" value="{{ val }}" {% if val == value|default:"" %}checked{% endif %}>{{ display }}</label></li>
{% endfor %}
</ul>
{% endblock %}

        ''',
    }
    PARTIALS = {
        'use_correct_block': "{% field form.name 'custom_input' %}",
        'unknown_block': "{% field form.name 'does_not_exist' %}",
        'auto_widget1': "{% field form.name %}",
        'auto_widget2': "{% field form.gender %}",
        'auto_widget3': "{% field form.is_cool %}",
        'force_text_widgets1': "{% field form.model %}",
        'force_text_widgets2': "{% field form.radio %}",
        'force_text_widgets3': "{% field form.multiple %}",
    }

    def test_use_correct_block(self):
        """
        Make sure the field tag uses the right block specified.
        """
        template = get_template('use_correct_block')
        result = template.render(self.context)
        self.assertEqual(result, """<input type="text" name="name" value="">""")

    def test_unknown_block(self):
        """
        Trying to render a block that doesn't exist raises an error.
        """
        template = get_template('unknown_block')
        with self.assertRaises(TemplateSyntaxError):
            template.render(self.context)

    def test_auto_widget(self):
        """
        Choose the correct widget according to the form field.

        """
        template = get_template('auto_widget1')
        self.assertEqual(
            template.render(self.context),
            """auto widget CharField_TextInput_name"""
        )

        template = get_template('auto_widget2')
        self.assertEqual(
            template.render(self.context),
            """auto widget ChoiceField_RadioSelect"""
        )

        template = get_template('auto_widget3')
        self.assertEqual(
            template.render(self.context),
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

        template = get_template('force_text_widgets1')
        expected_html = """<option value="2" selected>Two</option>"""
        self.assertInHTML(expected_html, template.render(ctx1))
        self.assertInHTML(expected_html, template.render(ctx2))

        # Test radio's
        template = get_template('force_text_widgets2')
        expected_html = """<label><input type="radio" id="id_radio_0" value="1" checked>One</label>"""
        self.assertInHTML(expected_html, template.render(ctx1))
        self.assertInHTML(expected_html, template.render(ctx2))

        # Test multiple
        template = get_template('force_text_widgets3')
        expected_html1 = """<option value="1" selected>One</option>"""
        expected_html2 = """<option value="2" selected>Two</option>"""
        self.assertInHTML(expected_html1, template.render(ctx1))
        self.assertInHTML(expected_html2, template.render(ctx1))
        self.assertInHTML(expected_html1, template.render(ctx2))
        self.assertInHTML(expected_html2, template.render(ctx2))


class UseTagTest(TemplateTestMixin, SimpleTestCase):
    """
    Tests for the {% use %} tag.

    """

    TEMPLATES = {
        'test.form': '''
{% block use_test %}{{ test }}{% endblock %}
{% block use_test_context %}{{ test }}{% endblock %}
        ''',
    }
    PARTIALS = {
        'use_tag': "{% use 'use_test' test='use tag test' %}",
        'use_tag_inherits_context': "{% use 'use_test_context' %}",
    }

    def test_use_tag(self):
        """
        Basic use tag usage.

        """
        template = get_template('use_tag')
        self.assertEqual(template.render(self.context), "use tag test")

    def test_use_tag_inherits_context(self):
        """
        Use tag should inherit context.

        """
        template = get_template('use_tag_inherits_context')
        context = Context({'test': 'use tag test'})
        self.assertEqual(template.render(context), 'use tag test')


class FlatAttrsFilterTest(TemplateTestMixin, SimpleTestCase):
    """
    Make sure our flatattrs filter works.

    """
    TEMPLATES = {
        'test.form': '''
''',
        'flat_attrs_filter': STOCK_TEMPLATE.format("""<input{{ attrs|flat_attrs }}>"""),
    }
    def test_flat_attrs_filter(self):
        """
        Flat attrs filter does what it's supposed to do.

        NOTE: Attributes are sorted alphabetically.

        """
        template = get_template('flat_attrs_filter')
        context = Context({'attrs': {
            'name': 'test',
            'id': 'id_test',
        }})
        self.assertEqual(template.render(context), """<input id="id_test" name="test">""")


class DefaultTemplateTest(SimpleTestCase):
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


class InheritanceTest(TemplateTestMixin, SimpleTestCase):
    """ Test that extending and block inheritance work correctly """
    TEMPLATE_BASE = '''{{% load formulation %}}{{% form 'test2.form' %}}{}{{% endform %}}'''
    TEMPLATES = {
        'test.form': '''
{% load formulation %}
{% block Inherited %}foo{% endblock %}
        ''',
        'test2.form': '''
{% extends "test.form" %}
{% load formulation %}

{% block Inherited %}{{ block.super }}bar{% endblock %}
        ''',
    }
    PARTIALS = {
        'inherited_form': '''{% field form.name 'Inherited' %}''',
    }

    def test_inherited_form(self):
        template = get_template('inherited_form')
        self.assertEqual(template.render(self.context), 'foobar')


class MultipleFormsTest(TemplateTestMixin, SimpleTestCase):
    """
    Test that multiple forms don't pollute each other.

    This is a regression test, since 2.0.8 block.super is possible, but
    context pollution happened causing the wrong blocks to be rendered.
    """
    TEMPLATE_BASE = "{0}"
    TEMPLATES = {
        'test.form': '''
{% block RecurringNode %}foo{% endblock %}
        ''',
        'test2.form': '''
{% extends 'test.form' %}
{% block RecurringNode %}bar{% endblock %}
        ''',
        'multiple_forms': '''
            {% load formulation %}
            {% form 'test.form' %}
            {% field form.name 'RecurringNode' %}
            {% endform %}
            {% form 'test2.form' %}
            {% field form.name 'RecurringNode' %}
            {% endform %}
        ''',
    }

    def test_multiple_forms(self):
        template = get_template('multiple_forms')
        rendered = template.render(self.context)
        self.assertIn('foo', rendered)
        self.assertIn('bar', rendered)
