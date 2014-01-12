# -*- coding: utf-8 -*-
"""
    controlbeast
    ~~~~~~~~~~~~

    :copyright: Copyright 2013, 2014 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
import os

VERSION = (0, 1, 0, 'alpha', 0)
COPYRIGHT = ('2013, 2014', 'the ControlBeast team')

DEFAULTS = {
    'scm': 'Git',
    'dir': {
        'repo': {
            'conf': 'conf',
            'hosts': 'hosts',
            'recipes': {
                'python': os.path.join('recipes', 'python'),
                'yaml': os.path.join('recipes', 'yaml')
            }
        },
        'host': {
            'base': 'base',
            'jails': 'jails',
            'conf': {
                'auto': os.path.join('conf', 'auto'),
                'custom': os.path.join('conf', 'custom')
            }
        }
    },
    'keystore': {
        'repo': {
            'name': 'keystore.sec',
            'location': 'dir.repo.conf'
        }
    }
}


def get_conf(key):
    """
    Get a global configuration value by its key. Nested keys are possible and need being separated by a dot.

    :param str key: string identifying the requested configuration value
    :returns the requested configuration value or None
    """
    keys = key.split('.')
    directory = DEFAULTS
    for k in keys:
        if k in directory:
            directory = directory[k]
        else:
            directory = None
            break

    if 'name' in directory and 'location' in directory:
        return os.path.join(get_conf(directory['location']), directory['name'])

    return directory


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