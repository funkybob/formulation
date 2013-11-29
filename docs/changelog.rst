=========
Changelog
=========

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

