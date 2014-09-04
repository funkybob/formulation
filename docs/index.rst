.. formulation documentation master file, created by
   sphinx-quickstart on Fri Nov 29 16:08:49 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Formulation
===========

.. rubric:: Putting form rendering in its place.

.. image:: https://travis-ci.org/funkybob/formulation.png
              :target: https://secure.travis-ci.org/funkybob/formulation.png?branch=master

.. image:: https://pypip.in/d/formulation/badge.png
              :target: https://crate.io/packages/formulation

.. image:: https://pypip.in/v/formulation/badge.png
              :target: https://crate.io/packages/formulation


Contents:

.. toctree::
   :maxdepth: 2

   tags
   templates
   extras
   thanks

   changelog

Overview
========

It's fairly well accepted, now, that having the form rendering decisions in
your code is less than ideal.

However, most template-based solutions wind up being slow, because they rely
on many templates per form.

Formulation works by defining all the widgets for your form in a single "widget
template", and loading it once for the form.

Installation
============

You can install formulation using:

.. code-block:: sh

    $ pip install formulation

You will need to add `'formulation'` to your `settings.INSTALLED_APPS`.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
