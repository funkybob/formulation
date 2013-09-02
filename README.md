# formulation

Django Form rendering helper tags


## Overview

It's fairly well accepted, now, that having the form rendering decisions in your code is less than ideal.

However, most template-based solutions wind up being slow, because they rely on many templates.

Formulation works by defining all the widgets for your form in a single "widget template", and loading it once for the form.

## Usage

First, write a template where each block is a way to render a field.

We'll start with a simple one, with one hardy, general purpose field block.  Let's call it `mytemplate.form`:

    {% block basic %}
    {% if not nolabel %}{{ form_field.label_tag }}{% endif %}
    <input type="{{ field_type|default:"text" }}" name="{{ html_name }}" id="{{ id }}" value="{{ value|default:"" }}" class="{{ css_classes }}">
    {{ help_text }}
    {% endblock %}

Then, in your own template:

    {% load formulation %}

    <form method="POST" ... >
    {% form "mytemplate.form" %}
    {% field "basic" form.foo %}
    {% field "basic" form.bar nolabel=True extra_classes="simple" %}
    {% field "basic" form.baz type='email' %}
    {% endform %}

You can think of the field tag as being like `{% include %}` but for blocks.

### `{% form %}`

The `{% form %}` tag loads the template, and puts its blocks in a dict in the context, called `widgets`.

#### Template Inheritance

You can still use {% extends %} in your widget templates, with one restriction: the template to extend MUST be known at parse time.  It may not be a variable.

    # Good
    {% extends "my/other.html" %}

    # BAD - Won't work!
    {% extends foo %}

This is because when the template is loaded and the blocks resolved, there is no Context in which to resolve the variable.

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


### `{% use %}`

You may have some chunks of templating that aren't fields, but are useful within the form.
For these, write them as blocks in your `xyz.form` template, then use the `{% use %}` to include them:

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

It works just like include, but will use a block from the current widget template.

## Other uses

Formulation is not limited to forms and fields.  There's no reason you can't also use it to abstract commonly used fragments of template code.

    {% form "widgets.form" %}

    {% use "framed-box" title="Some box!" %}

    ...

    {% endform %}

## Thanks!

- kezabelle for the name
- bradleyayers for ideas on supporting multiple fields.
- SmileyChris for the idea to hoik useful values off the field and into context

