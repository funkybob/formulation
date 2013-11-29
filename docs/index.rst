.. formulation documentation master file, created by
   sphinx-quickstart on Fri Nov 29 16:08:49 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to formulation's documentation!
=======================================

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
on many templates.

Formulation works by defining all the widgets for your form in a single "widget
template", and loading it once for the form.

Installation
============

You can install formulation using:

    $ pip install formulation

You will need to add `'formulation'` to your `settings.INSTALLED_APPS`.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
