# -*- coding: utf-8 -*-
"""
    controlbeast.utils.compat
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""


def __local_set_inheritable(fd, inheritable):
    """
    Dummy implementation of set_inheritable that actually does not do anything.
    This function will be used for Python versions < 3.4
    """
    pass


# Provide a set_inheritable implementation also for Python versions prior 3.4
try:
    from os import set_inheritable
except ImportError:
    set_inheritable = __local_set_inheritable