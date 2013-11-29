=========
Templates
=========

Formulation ships with a sample template which tries to emulate the default
Django form rendering as closely as possible.

The base field (called "input") looks like this:

.. code-block:: html

    {% block input %}
    {% use "_label" %}
    {% with field_type=field_type|default:"text" %}
    <input type="{{ field_type }}"
        name="{{ html_name }}"
        id="{{ id }}"
        value="{{ value|default:"" }}"
        class="{{ css_classes }} {{ errors|yesno:"error," }}"
        {{ widget.attrs|flat_attrs }}
        {{ required|yesno:"required," }}
        {{ autofocus|yesno:"autofocus," }}
        {% if placeholder %}placeholder="{{ placeholder }}"{% endif %}
    >
    {% endwith %}
    {% use "_help" %}
    {% use "_errors" %}
    {% endblock %}

There are 3 supplementary blocks it uses, making it easier for you to customise
rendering without having to rewrite the whole template.

.. code-block:: html

    {% block _label %}
    {% if label %}<label id="{{ id_for_label }}" for="{{ id }}">{{ label }}</label>{% endif %}
    {% endblock %}

.. code-block:: html

    {% block _help %}
    {{ help_text }}
    {% endblock %}

.. code-block:: html

    {% block _errors %}
    {% if errors %}
    <ul class="errorlist">
    {% for error in errors %}
        <li class="error">{{ error }}</li>
    {% endfor %}
    </ul>
    {% endif %}
    {% endblock %}

Examples
========

It can be helpful to look at how some of the default widgets are implemented to
see how simple it can be.

.. code-block:: html

    {% block TextInput %}{% use "input" %}{% endblock %}

The basic TextInput uses the input widget without any alterations.

.. code-block:: html

    {% block EmailInput %}{% use "input" field_type="email" %}{% endblock %}

The EmailInput simply provides an override for field_type.

.. code-block:: html

    {% block PasswordInput %}{% use "input" field_type="password" value="" %}{% endblock %}

PasswordInput ensures the value is blanked out.

.. code-block:: html

    {% block DateInput %}{% use "input" field_type="date" value=value|date:'Y-m-d' %}{% endblock %}

DateInput, as well as DateTimeInput and TimeInput, use the ``date`` filter to
convert the value to a userful format.

