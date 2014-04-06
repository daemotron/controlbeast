# -*- coding: utf-8 -*-
"""
    controlbeast.scm
    ~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""


from controlbeast.scm.base import CbSCMWrapper
from controlbeast.utils import loader
from controlbeast.conf import get_conf

_scm_wrappers = None
_scm_handler = None


# convenience imports
from controlbeast.scm.base import CbSCMError
from controlbeast.scm.base import CbSCMBinaryError
from controlbeast.scm.base import CbSCMInitError
from controlbeast.scm.base import CbSCMCommitError
from controlbeast.scm.base import CbSCMBranchError
from controlbeast.scm.base import CbSCMCheckoutError
from controlbeast.scm.base import CbSCMRepoError


def _load_scm_handler():
    """
    Load and instantiate scm wrapper class for function style interface
    """
    global _scm_handler
    if not _scm_handler:
        scm_class = get_scm(get_conf('SCM_CLASS'))
        _scm_handler = scm_class()


def load_scm():
    """
    Detect available scm modules or packages and store result in the _scm_wrappers variable
    """
    global _scm_wrappers
    _scm_wrappers = loader.detect_class_modules('controlbeast.scm', parent=CbSCMWrapper)


def get_scm(scm_name):
    """
    Get a SCM wrapper class by its name.

    :param str scm_name: The name or alias of the SCM wrapper class to be loaded
    :return: SCM wrapper class reference which can be instantiated
    """
    global _scm_wrappers
    if not _scm_wrappers:
        load_scm()

    if not _scm_wrappers:
        return None

    if scm_name in _scm_wrappers:
        return loader.load_member(_scm_wrappers[scm_name], scm_name)
    else:
        return None


def scm_init(*args, **kwargs):
    """
    Initialise a new SCM repository.

    :param str path: Path on the file system where the repository should reside. If not specified, it defaults to the
                     current work directory.
    """
    if not _scm_handler:
        _load_scm_handler()

    _scm_handler.init(*args, **kwargs)


def scm_commit(*args, **kwargs):
    """
    Commit content of an existing SCM repository.

    :param str path:    Path on the file system where the repository resides. If not specified, it defaults to the
                        current work directory.
    :param str message: Commit message to be attached to the commit record.
    """
    if not _scm_handler:
        _load_scm_handler()

    _scm_handler.commit(*args, **kwargs)


def scm_create_branch(*args, **kwargs):
    """
    Create a branch within an existing SCM repository.

    :param str path:    Path on the file system where the repository resides. If not specified, it defaults to the
                        current work directory.
    :param str name:    Name of the branch to be created.
    """
    if not _scm_handler:
        _load_scm_handler()

    _scm_handler.create_branch(*args, **kwargs)


def scm_get_branches(*args, **kwargs):
    """
    Get a list of branches existing within the repository.

    :param str path:    Path on the file system where the repository resides. If not specified, it defaults to the
                        current work directory.
    :return:            list of branch names
    :rtype:             list
    """
    if not _scm_handler:
        _load_scm_handler()

    return _scm_handler.get_branches(*args, **kwargs)


def scm_get_active_branch(*args, **kwargs):
    """
    Get the active named branch of an existing SCM repository.

    :param str path:    Path on the file system where the repository resides. If not specified, it defaults to the
                        current work directory.
    :return:            Name of the active branch
    :rtype:             str
    """
    if not _scm_handler:
        _load_scm_handler()

    return _scm_handler.get_active_branch(*args, **kwargs)


def scm_checkout(*args, **kwargs):
    """
    Check out a branch within a git repository.

    :param str path:    Path on the file system where the repository resides. If not specified, it defaults to the
                        current work directory.
    :param str name:    Name of the branch to be checked out.
    """
    if not _scm_handler:
        _load_scm_handler()

    _scm_handler.checkout(*args, **kwargs)


def scm_get_root(*args, **kwargs):
    """
    Get the path to the root of an existing SCM repository.

    :param str path:    Path on the file system where to start looking for the repository's root directory

    :returns:           Path to the root of an existing SCM repository.
    :rtype:             str
    """
    if not _scm_handler:
        _load_scm_handler()

    return _scm_handler.get_root(*args, **kwargs)
