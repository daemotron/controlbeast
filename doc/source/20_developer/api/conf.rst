ControlBeast Configuration
==========================

Configuration Object
--------------------

.. currentmodule:: controlbeast.conf

.. autoclass:: CbConf
   :members:


ControlBeast Configuration Attributes
-------------------------------------

.. currentmodule:: controlbeast.conf.default

All default configuration information is centralized within the :py:mod:`controlbeast.conf.default` module.
All configuration directives being present within this module have to be written in upper case letters. This
being the case, they will automatically be taken into consideration by the :py:class:`~controlbeast.conf.CbConf`
class instance.

Core Configuration Attributes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. py:data:: DEFAULT_CHARSET

   Default character set to be used for any byte sequence / string conversion operations


SCM Configuration Attributes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. py:data:: SCM_CLASS

   Version management system implementation to be used