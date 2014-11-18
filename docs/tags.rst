=============
Template Tags
=============

Formulation works by providing a number of template tags.


The ``form`` tag
================

The ``form`` tag loads the template, and puts its blocks in a dict in the
context, called `formulation`.  You typically won't access this directly, as
it's raw BlockNode instances.

.. code-block:: html+django

    {% form "widgets/bootstrap.form" %}
    ...
    {% endform %}

You can optionally pass the form you will be using, also.  This will allow the
``field`` tag to reference fields by name, instead of instance.

.. note:: There is a default form template, called "formulation/default.form",
   provided that should emulate the stock Django widgets.

Template inheritance
--------------------

Widget templates are just normal templates, so {% extends %} still works as
expected.  This lets you define a base, common form template, and localised
extensions where you need.


The ``field`` tag
=================

Used to render a form field, optionally specifying the widget to use.

.. code-block:: html+django

    {% field formfield [widget name] [key=value...] %}

You can think of the field tag as being like `{% include %}` but for blocks.
However, it also adds many attributes from the form field into the context.

Values from ``BoundField``
--------------------------

The following values are take from the ``BoundField``:

- css_classes
- errors
- field
- form
- help_text
- html_name
- id_for_label
- label
- name
- value

Values from ``Field``
---------------------

And these from the ``Field`` itself:

- choices
- widget
- required

Any extra keyword arguments you pass to the field tag will overwrite values of the same name.

Auto-widget
-----------

If you omit the widget in the {% field %} tag, formulation will try to
auto-detect the block to use.  It does so by looking for the first block to
match one of the following patterns:

- {field}_{widget}_{name}
- {field}_{name}
- {widget}_{name}
- {field}_{widget}
- {name}
- {widget}
- {field}

Where 'field' is the form field class (e.g. CharField, ChoiceField, etc),
'widget' is the widget class name (e.g. NumberInput, DateTimeInput, etc) and
'name' is the name of the field.

If no block is found, a TemplateSyntaxError is raised.


The ``use`` tag
===============

You may have some chunks of templating that aren't fields, but are useful
within the form.  For these, write them as blocks in your `xyz.form` template,
then use the `{% use %}` to include them:

demo.html
---------

.. code-block:: html+django

    {% form "demo.form" %}
    ...
    {% use "actions" submit="Update" %}
    {% endform %}

demo.form
---------

.. code-block:: html+django

    {% block actions %}
    <div class="actions">
        <input type="submit" value="{{ submit|default:"Save" }}">
        <a href="/">Cancel</a>
    </div>
    {% endblock %}

It works just like include, but will use a block from the current widget
template.

