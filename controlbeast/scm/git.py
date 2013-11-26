# -*- coding: utf-8 -*-
"""
    controlbeast.scm.git
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""

from controlbeast.scm.base import CbSCMWrapper


class Git(CbSCMWrapper):
    """
    Class acting as wrapper for the git command line interface
    """

    _scm_binary_name = 'git'
