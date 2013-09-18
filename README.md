# formulation

Django Form rendering helper tags


## Overview

It's fairly well accepted, now, that having the form rendering decisions in
your code is less than ideal.

However, most template-based solutions wind up being slow, because they rely
on many templates.

Formulation works by defining all the widgets for your form in a single "widget
template", and loading it once for the form.

## Usage

First, write a template where each block is a way to render a field.

We'll start with a simple one, with one hardy, general purpose field block.
Let's call it `mytemplate.form`:

    {% block basic %}
    {% if not nolabel %}{{ form_field.label_tag }}{% endif %}
    <input
        type="{{ field_type|default:"text" }}"
        name="{{ html_name }}"
        id="{{ id }}"
        value="{{ value|default:"" }}"
        class="{{ css_classes }}"
        {{ required|yesno:"required," }}
    >
    {{ help_text }}
    {% endblock %}

Then, in your own template:

    {% load formulation %}

    <form method="POST" ... >
    {% form "mytemplate.form" %}
    {% field form.foo "basic" %}
    {% field form.baz "basic" type='email' %}
    {% endform %}

You can think of the field tag as being like `{% include %}` but for blocks.

### `{% form %}`

The `{% form %}` tag loads the template, and puts its blocks in a dict in the
context, called `formulation`.  You typically won't access this directly, as
it's raw BlockNode instances.

    {% form "widgets/bootstrap.form" %}
    ...
    {% endform %}


#### Template Inheritance

Widget templates are just normal templates, so {% extends %} still works as
expected.  This lets you define a base, common form template, and localised
 extensions where you need.

### `{% field %}`

Each time you use the `{% field %}` tag, it renders the block specified.

It's easy to extend this to more complex field types:

    {% block TypedChoiceField %}
    {% if not nolabel %}
    <label for="{{ id }}" {% if required %}class="required"{% endif %}> {{ label }} </label>
    {% endif %}
    <select name="{{ html_name }}" id="{{ id }}" {% if errors %}class="error"{% endif %}>
    {% for option_value, option_label in choices %}
    <option value="{{ option_value }}" {% if value == option_value %}selected="selected"{% endif %}>{{ option_label }}</option>
    {% endfor %}
    </select>
    {{ help_text }}
    {% endblock %}

### Auto-widget

If you omit the widget in the {% field %} tag, formulation will try to
auto-detect the block to use.  It does so by looking for the first block to
match one of the following patterns:

    '{field}_{widget}_{name}'
    '{field}_{name}'
    '{widget}_{name}'
    '{field}_{widget}'
    '{name}'
    '{widget}'
    '{field}'

Where 'field' is the form field class (e.g. CharField, ChoiceField, etc),
'widget' is the widget class name (e.g. NumberInput, DateTimeInput, etc) and
'name' is the name of the field.

If no block is found, a TemplateSyntaxError is raised.

### `{% use %}`

You may have some chunks of templating that aren't fields, but are useful
within the form.  For these, write them as blocks in your `xyz.form` template,
then use the `{% use %}` to include them:

    # demo.html
    {% form "demo.form" %}
    ...
    {% use "actions" submit="Update" %}
    {% endform %}

    # demo.form
    {% block actions %}
    <div class="actions">
        <input type="submit" value="{{ submit|default:"Save" }}">
        <a href="/">Cancel</a>
    </div>
    {% endblock %}

It works just like include, but will use a block from the current widget
template.

## Extras

There is also the `{% reuse %}` template tag, which allows you to reuse any
template block within the current template [as opposed to the form widget
template] like a macro.  Again, it follows the same syntax as the {% include %}
tag:

    {% load reuse %}
    {% reuse "otherblock" foo=1 %}

## Other uses

Formulation is not limited to forms and fields.  There's no reason you can't
also use it to abstract commonly used fragments of template code.

    {% form "widgets.form" %}

    {% use "framed-box" title="Some box!" %}

    ...

    {% endform %}

## Thanks!

- kezabelle for the name
- bradleyayers for ideas on supporting multiple fields.
- SmileyChris for the idea to "explode" fields into the context

