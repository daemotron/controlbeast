# -*- coding: utf-8 -*-
"""
    controlbeast.conf.global
    ~~~~~~~~~~~~~~~~~~~~~~~~

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