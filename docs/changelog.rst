=========
Changelog
=========

v2.0.13
=======

Bugs Fixed:

- Make field tag less agressive about applying force_text to values
  [Thanks Sergei Martens]

v2.0.12
=======

Features added:

- Added "widget_type" and "field_type" to exploded field data.
- Added "display" value to exploded field data for fields with choices.
- Move 'choices' handling out of inner loop
- Improve error message when widget can't be found.

Bugs Fixed:

- Fixed handling of multi-value fields
- Fixed default values for 'value' in default template.

v2.0.11
=======

Bugs Fixed:

- Use the "new" method of request_context instead of deep copy. [Fixes #23]
- Refactor tests to make easier to run

v2.0.10
=======

Bugs Fixed:

- One more change to BlockContext handling. [More thanks to Sergei Maertens]

v2.0.9
======

Bugs Fixed:

- Fix dirty BlockContext issue introduced in 2.0.8 [Thanks Sergei Maertens]
- Removed undocumented render_form


v2.0.8
======

Bugs Fixed:

- Ensure value is a comparable type in choices widgets
- Fixed default widget for select types to include display string
- Allow {{ block.super }} to work

v2.0.7.1
========

Bugs Fixed:

- Change list() to [] to not turn strings into lists

v2.0.7
======

Bugs Fixed:

- Fixed renamed variables in reuse tag
- Fixed testing current value in Select widget template
- Fixed value in Checkbox widget template
- force_text on choices values

Enhancements:

+ Improved documentation
+ Improved test coverage

Thanks to jwa

v2.0.6
======

Bugs Fixed:

- Removed duplicate EmailField block

Enhancements:

+ Changed to using contextlib
+ Allow a list of block names to be passed to {% reuse %}
+ Added sphinx docs
+ Added field lookup by name

v2.0.5
======

Bugs Fixed:

- Packaging fix

Enhancements:

+ Improved docs
+ Added {% render_form %} tag

v2.0.4
======

Bugs Fixed:

- Fixed date/time formatting in default template

v2.0.3
======

Bugs Fixed:

- Added tests (thanks jwa!)
- Fixed auto widget (thanks jwa!)

Enhancements:

+ Improved templates (thanks jwa!)
+ Began Py3 compatibility (thanks jwa!)

v2.0.2
======

Bugs Fixed:

- Fix importing of form.util(s) to make Django 1.5 compatible

v2.0.1
======

Bugs Fixed:

- Fixed context over-stacking (#5)

Enhancements:

+ Added ``flat_attrs`` filter
+ Changed default template to include templates for all stock Django widgets

v2.0.0
======

Enhancements:

+ Changed to explode field and widget attributes into the context

