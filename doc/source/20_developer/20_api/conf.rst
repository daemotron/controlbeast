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

.. automodule:: controlbeast.conf.default

All default configuration information is centralized within the :py:mod:`~controlbeast.conf.default` module.
All configuration directives being present within this module have to be written in upper case letters. This
being the case, they will automatically be taken into consideration by the :py:class:`~controlbeast.conf.CbConf`
class instance.

Core Configuration Attributes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. py:data:: DEFAULT_CHARSET

   Default character set to be used for any byte sequence / string conversion operations

.. py:data:: TEMPLATE_PATH

   Default location for templates


SCM Configuration Attributes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. py:data:: SCM_CLASS

   Version management system implementation to be used

.. py:data:: SCM_BRANCH

   Default branch to be used for creating new host systems


Host Configuration Attributes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. py:data:: HOST_FS_FILE

   Name of the YAML file containing hard disk and file system configuration

.. py:data:: HOST_NETWORK_FILE

   Name of the YAML file containing network configuration

.. py:data:: HOST_OS_FILE

   Name of the YAML file containing OS configuration

.. py:data:: HOST_RESCUE_FILE

   Name of the YAML file containing rescue system configuration

.. py:data:: HOST_SERVICE_FILE

   Name of the YAML file containing service configuration
