# -*- coding: utf-8 -*-
"""
    controlbeast.scm
    ~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""


from controlbeast.scm.base import CbSCMWrapper
from controlbeast.utils import loader

_scm_wrappers = None


def load_scm():
    """
    Detect available scm modules or packages and store result in the _scm_wrappers variable
    """
    global _scm_wrappers
    _scm_wrappers = loader.detect_class_modules('controlbeast.scm', parent=CbSCMWrapper)


def get_scm(scm_name):
    """
    Get a SCM wrapper class by its name.

    :param scm_name: The name or alias of the SCM wrapper class to be loaded
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