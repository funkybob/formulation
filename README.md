# formulation

Django Form rendering helper tags


## Overview

It's fairly well accepted, now, that having the form rendering decisions in your code is less than ideal.

However, most template-based solutions wind up being slow, because they rely on many templates.

Formulation works by defining all the widgets for your form in a single "widget template".

## Usage

First, write a template where each block is a way to render a field.

We'll start with a simple one, with one hardy, general purpose field block.  Let's call it `mytemplate.form`:

    {% block basic %}
    {% if not nolabel %}
    <label for="{{ field.auto_id }}" {% if field.required %}class="required"{% endif %}> {{ label|default:field.label }} </label>
    {% endif %}
    <input type="{{ field_type|default:"text" }}" name="{{ field.html_name }}" id="{{ field.auto_id }}" value="{{ field.value|default:"" }}" {% if field.errors %}class="error"{% endif %} />
    {{ field.help_text }}
    {% endblock %}

Then, in your own template:

    {% load formulation %}

    <form method="POST" ... >
    {% form "mytemplate.form" %}
    {% field "basic" form.foo %}
    {% field "basic" form.bar nolabel=True %}
    {% field "basic" form.baz type='email' %}
    {% endform %}

Yep, it's that simple.

The `{% form %}` tag loads the template, and puts its blocks in a dict in the context, called `widgets`.

You can even use template inheritance, just as normal.

Each time you use the `{% field %}` tag, it renders the block.

It's easy to extend this to more complex field types:

    {% block TypedChoiceField %}
    {% if not nolabel %}
    <label for="{{ field.id }}" {% if field.required %}class="required"{% endif %}> {{ field.label }} </label>
    {% endif %}
    <select name="{{ field.html_name }}" id="{{ field.auto_id }}" {% if field.errors %}class="error"{% endif %}>
    {% for option_value, option_label in field.field.choices %}
    <option value="{{ option_value }}" {% if field.value == option_value|safe %}selected="selected"{% endif %}>{{ option_label }}</option>
    {% endfor %}
    </select>
    {{ field.help_text }}
    {% endblock %}

You can pass multiple form fields as positional arguments. They're put into a list and accessible via `fields`:

    # example.html
    {% form "mytemplate.form" %}
    {% field "multiwidget" field1 field2 ... %}
    ...
    {% endform %}
    
    # mytemplate.form
    {% block multiwidget %}
    {% for field in fields %}
    ...
    {% endfor %}
    {% endblock %}

The first field is still accessible as `field`.

### `{% use %}`

You may have some chunks of templating that aren't fields, but are useful within the form.
For these, write them as blocks in your `xyz.form` template, then use the `{% use %}` to include them:

    # demo.html
    {% form "demo.form %}
    ...
    {% use "actions" submit="Update" %}
    {% endform %}

    # demo.form
    {% block actions %}
    <div class="actions">
        <input type="submit" value="{{ submit|default:"Save" }}"/>
        <a href="/">Cancel</a>
    </div>
    {% endblock %}

It works just like include, but will use a block from the current widget template.

## Thanks!

- kezabelle for the name
- bradleyayers for ideas on supporting multiple fields.


