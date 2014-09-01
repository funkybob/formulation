from django.template import Context
from django.template.loader import get_template
from django.test import SimpleTestCase


class InheritanceTests(SimpleTestCase):

    def test_inheritance(self):
        """
        Regression: in templates where blocks follow the block where the form
        ends up, overriding them has no effect. See testcase, the block 'two'
        is not overridden when formulaion forms are present.
        """
        tpl = get_template('inherited.html')
        render = tpl.render(Context())
        self.assertInHTML('<div>overridden</div>', render)
