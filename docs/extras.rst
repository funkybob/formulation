======
Extras
======

The ``flat_attrs`` filter
=========================

This is simply a wrapper around ``from django.forms.utils import flatatt``

It converts a dict of attributes into a string, in propert key="value" syntax.
The values will be escaped, but keys will not.


The ``reuse`` tag
=================

There is also the `{% reuse %}` template tag, which allows you to reuse any
template block within the current template [as opposed to the form widget
template] like a macro.  Again, it follows the same syntax as the {% include %}
tag:

    {% load reuse %}
    {% reuse "otherblock" foo=1 %}

You can also pass a list of block names to search; first found will be used.


Using ``use`` for macros
========================

Formulation is not limited to forms and fields.  There's no reason you can't
also use it to abstract commonly used fragments of template code.

    {% form "widgets.form" %}

    {% use "framed-box" title="Some box!" %}

    ...

    {% endform %}

