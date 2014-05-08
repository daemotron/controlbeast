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

.. autofunction:: scm_create_branch

.. autofunction:: scm_get_branches

.. autofunction:: scm_get_active_branch

.. autofunction:: scm_checkout

.. autofunction:: scm_get_root


Exceptions
----------

.. currentmodule:: controlbeast.scm.base

.. autoexception:: CbSCMError
   :members:
   :private-members:

.. autoexception:: CbSCMBinaryError
   :members:
   :private-members:

.. autoexception:: CbSCMInitError
   :members:
   :private-members:

.. autoexception:: CbSCMCommitError
   :members:
   :private-members:

.. autoexception:: CbSCMBranchError
   :members:
   :private-members:

.. autoexception:: CbSCMCheckoutError
   :members:
   :private-members:

.. autoexception:: CbSCMRepoError
   :members:
   :private-members:


Git SCM Interface
-----------------

.. currentmodule:: controlbeast.scm.git

.. automodule:: controlbeast.scm.git

.. autoclass:: Git
   :members:
   :private-members:
