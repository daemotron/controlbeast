Project Hosting
===============

ControlBeast uses `Git`_ as its SCM. The project's "blessed" Git repository resides at `GitHub`_. It is publicly
accessible, but only core maintainers can commit to this blessed repository.


Repository Structure
--------------------

Within the project's main directory (or `repository`_ root), code and documentation are organised within four
directories:

* ``controlbeast`` is the Python package containing all the project's production code
* ``doc`` is a directory (not a Python package) containing the project's `Sphinx`_ documentation
* ``scripts`` is a directory (not a Python package) containing executable Python scripts
* ``test`` is the Python package containing all the project's unit tests


Commit Rules
------------

Each commit done to the blessed repository must contain only working code, which in particular means:

* All unit tests run without error and green result
* The code does not contain any FIXME tags
* The code may however still contain TODO tags


Automated Testing
-----------------

Each commit submitted to the blessed repository is subject to automated unit testing. The automated execution of all
unit tests is triggered by a Git hook and performed by the `Travis CI`_ platform.


.. _Git: http://git-scm.com/
.. _GitHub: https://github.com/daemotron/controlbeast
.. _repository: https://github.com/daemotron/controlbeast
.. _Sphinx: http://sphinx-doc.org
.. _Travis CI: https://travis-ci.org/daemotron/controlbeast
