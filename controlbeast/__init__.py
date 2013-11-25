# -*- coding: utf-8 -*-
"""
    controlbeast
    ~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""

VERSION = (0, 1, 0, 'alpha', 0)
COPYRIGHT = ('2013', 'the ControlBeast team')

def get_version(*args, **kwargs):
    """
    Returns PEP 386 compliant version number for the Pytain package
    """
    from controlbeast.utils.version import get_version
    return get_version(*args, **kwargs)