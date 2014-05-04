# -*- coding: utf-8 -*-
"""
    controlbeast.conf.default
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""


import os


# Default ControlBeast settings.

# CORE Settings
###############

# Default character set to be used for any byte sequence / string conversion operations
DEFAULT_CHARSET = 'utf-8'

# Default location for templates
TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')


# REPOSITORY Settings
#####################

# Version management system implementation to be used
SCM_CLASS = 'Git'

# Default branch to be used for creating new host systems
SCM_BRANCH = 'master'


# HOST Settings
###############

# Name of the YAML file containing network configuration
HOST_NETWORK_FILE = os.path.join('base', 'network.yml')

# Name of the YAML file containing rescue system configuration
HOST_RESCUE_FILE = os.path.join('base', 'rescue.yml')

# Name of the YAML file containing hard disk and file system configuration
HOST_FS_FILE = os.path.join('base', 'fs.yml')

# Name of the YAML file containing OS configuration
HOST_OS_FILE = os.path.join('base', 'os.yml')

# Name of the YAML file containing service configuration
HOST_SERVICE_FILE = os.path.join('base', 'service.yml')
