# -*- coding: utf-8 -*-
"""
    controlbeast
    ~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""

VERSION = (0, 1, 0, 'alpha', 0)
COPYRIGHT = ('2013', 'the ControlBeast team')

DEFAULTS = {
    'scm': 'Git'
}


def get_conf(key):
    """
    Get a global configuration value by its key

    :param str key: string identifying the requested configuration value
    :returns the requested configuration value or None
    """
    if key in DEFAULTS:
        return DEFAULTS[key]
    else:
        return None


def get_version(*args, **kwargs):
    """
    Returns PEP 386 compliant version number for the Pytain package
    """
    from controlbeast.utils.version import get_version
    return get_version(*args, **kwargs)