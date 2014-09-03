from django.template import Context
from django.template.loader import get_template
from django.test import SimpleTestCase
from django.test.utils import setup_test_template_loader, restore_template_loaders


TEMPLATES = {
    'formulation/default.form': '''
''',
    'base.html': '''
{% block one %}<span>one</span>{% endblock %}
{% block form %}{% endblock %}
{% block two %}<div>two</div>{% endblock %}
''',
    'inherited.html': '''
{% extends "base.html" %}
{% load formulation %}
{% block form %}
    {% form 'formulation/default.form' %}
        <form>empty</form>
    {% endform %}
{% endblock %}
{% block two %}<div>overridden</div>{% endblock %}
''',
}


class InheritanceTests(SimpleTestCase):

    @classmethod
    def setUpClass(cls):
        setup_test_template_loader(TEMPLATES)

    @classmethod
    def tearDownClass(cls):
        restore_template_loaders()

    def test_inheritance(self):
        """
        Regression: in templates where blocks follow the block where the form
        ends up, overriding them has no effect. See testcase, the block 'two'
        is not overridden when formulaion forms are present.
        """
        tpl = get_template('inherited.html')
        render = tpl.render(Context())
        self.assertInHTML('<div>overridden</div>', render)
