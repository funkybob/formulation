formulation
===========

Django Form rendering helper tags


Usage
=====

First, write a template where each block is a way to render a field.

We'll start with a simple one, with one hardy, general purpose field block.  Let's call it "mytemplate.form":

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

Want more complex field types:

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

Also, to help with repeated block, there's the "use" tag.

    {% use "other" foo="bar" baz=quux %}

It works just like include, but will use a block from the current widget template.

Thanks!
=======

Thanks to kezabelle for the name!

