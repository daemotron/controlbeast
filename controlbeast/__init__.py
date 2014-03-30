# -*- coding: utf-8 -*-
"""
    controlbeast
    ~~~~~~~~~~~~

    :copyright: Copyright 2013, 2014 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""


VERSION = (0, 1, 0, 'alpha', 0)
COPYRIGHT = ('2013, 2014', 'the ControlBeast team')


def get_version(*args, **kwargs):
    """
    Returns PEP 386 compliant version number for the ControlBeast package
    """
    from controlbeast.utils.version import get_version
    return get_version(*args, **kwargs)


def get_development_status(*args, **kwargs):
    """
    Returns PEP 301 compliant development status trove identifier for the ControlBeast package
    """
    from controlbeast.utils.version import get_development_status
    return get_development_status(*args, **kwargs)