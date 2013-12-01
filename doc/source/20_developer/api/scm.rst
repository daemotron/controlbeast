ControlBeast Version Management Interface
=========================================

General SCM Interface
---------------------

.. currentmodule:: controlbeast.scm

.. automodule:: controlbeast.scm

.. autofunction:: get_scm

.. autoclass:: CbSCMWrapper
   :members:
   :private-members:

Function-oriented Interface
---------------------------

.. autofunction:: scm_init

.. autofunction:: scm_commit


Exceptions
----------

.. currentmodule:: controlbeast.scm.base

.. autoclass:: CbSCMError
   :members:
   :private-members:

.. autoclass:: CbSCMBinaryError
   :members:
   :private-members:

.. autoclass:: CbSCMInitError
   :members:
   :private-members:

.. autoclass:: CbSCMCommitError
   :members:
   :private-members:

Git SCM Interface
-----------------

.. currentmodule:: controlbeast.scm.git

.. automodule:: controlbeast.scm.git

.. autoclass:: Git
   :members:
   :private-members:
