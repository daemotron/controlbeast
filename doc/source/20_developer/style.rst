Style Guide for ControlBeast Development
========================================


Introduction
------------

In brief: stick to `PEP 8`_ and `PEP 257`_, and you will be fine in 99% of all cases that may occur. But since those
two PEPs only refer to code style and inline documentation, you might want to continue reading this style guide,
particularly considering the sections on unit tests and documentation.


Python Compatibility
--------------------

ControlBeast's code has to be compatible with Python 3.3 or newer versions. There is no need for backwards compatibility
to Python's 2.x branches. In consequence, all functions, classes, data types etc. available either built-in or by the
Python standard library may be used. However, functions, classes, data types etc. introduced with a Python version
newer than 3.3 may **not** be used or have to be wrapped by a compatibility layer.


Using Libraries
---------------

Functionality provided by the Python standard library may be used without any further restriction (apart from the
Python version restriction indicated above). In order to avoiding a dependency hell, using third party libraries
should strictly be limited to cases where the third party library

* is written in pure Python code
* is well documented
* is actively maintained
* has a stable API
* is available via the `Python Package Index`_

Any third party library usage needs to be announced within these documents:

* Installation dependencies (``controlbeast/doc/source/10_user/install.rst``)
* Travis CI configuration (``controlbeast/.travis.yml``)


Code Style
----------

In general, `PEP 8`_ really covers what needs being said about code style. However, there are some points that might
need clarification; in particular when to deviate from the `PEP 8`_ instructions...

Indentation
~~~~~~~~~~~

As specified by `PEP 8`_, the general rule is to use 4 spaces (no tabs!) for code indentation. However, in multi-line
constructs it is *mandatory* to line up the closing brace/bracket/parenthesis with the first character of the line
where the multi-line construct was started::

   my_dict = {
       'foo': 'bar',
       'goo': 'baz',
   }

Source File Encoding
~~~~~~~~~~~~~~~~~~~~

All source files must be encoded in UTF-8 *without* BOM, and introduce their encoding in the first line::

   # -*- coding: utf-8 -*-

   # ... more stuff that's not interesting right now...

The only exception from this mandatory file header is a completely empty file such as an ``__init__.py`` file
bearing no code at all. In this specific case, the file size has to be zero bytes.

Import Statements
~~~~~~~~~~~~~~~~~

In general, following the rules as specified in `PEP 8`_ should generate compliant code. However, relative imports
should be avoided, even if the import statement will grow in length::

   # not ok
   from . import something

   # ok
   import controlbeast.something

Furthermore, importing with an alias name should be avoided::

   # not ok
   from controlbeast.something import SomeClass as OtherClass

   # ok
   from controlbeast.something import SomeClass


Inline Documentation
--------------------

All functions, classes, methods and class members must be documented using Python docstrings. All docstrings (except
those for class members) have to be written as multi-line docstrings, surrounded with three double quotes on a separate
line::

   class foo:
       """
       This is the foo class' docstring
       """

       #: I am the docstring of a class member
       _foo = 'bar'

       def __init__(self):
           """
           I am the class constructor's docstring
           """

The following rules shall be regarded when writing docstrings:

* Methods and functions docstrings shall document all arguments (except ``self``) by the ``:param <type> <name>:
  description`` statement
* Constructor parameters shall be documented in the class' docstring instead of the constructor's docstring
* Methods and functions (except properties) returning something shall document their return behaviour by the
  ``:returns <description>`` statement.


API Documentation
-----------------

All packages, modules, classes, exceptions and functions defined within the ``controlbeast`` package must be documented
within the ControlBeast API documentation. The minimum documentation would be one of the *autodoc* variants offered
by `Sphinx`_, e. g. ``.. autoclass:: classname``.


Unit Testing
------------

All classes, exceptions, methods and functions defined within the ``controlbeast`` package shall be covered by a
corresponding unit test. All unit tests are located within the ``test`` package. The structure of the ``test`` package
shall mirror the structure of the ``scripts`` directory and the ``controlbeast`` package. To avoid namespace conflicts,
all subpackages within the ``test`` package shall be prefixed with ``t_``.

Actual test classes have to inherit from :class:`unittest.TestCase` and be defined within a Python module named
``test_*.py``, where ``*`` should be seen as a wild card indicating the module or class being tested with the test
cases defined within this module.

.. note::

   All unit tests following the above given guidelines will be automatically detected and run by the unit test script
   ``scripts/ut.py`` when executed. This script is used for automated testing using the `Travis CI`_ platform.

Corresponding to the ``controlbeast`` package's API documentation, all unit tests shall be documented within the
ControlBeast test documentation using at least the *autodoc* functionality provided by `Sphinx`_.


.. _PEP 8: http://www.python.org/dev/peps/pep-0008/
.. _PEP 257: http://www.python.org/dev/peps/pep-0257/
.. _Python Package Index: https://pypi.python.org/pypi
.. _Sphinx: http://sphinx-doc.org
.. _Travis CI: https://travis-ci.org/daemotron/controlbeast
