# -*- coding: utf-8 -*-
"""
    controlbeast.cli.init
    ~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
import os

import controlbeast.cli.base
from controlbeast.scm import scm_init, CbSCMBinaryError, CbSCMInitError


class InitCommand(controlbeast.cli.base.CbCommand):
    """
    Command class implementing the init command
    """

    _help = 'Initialise ControlBeast repository'
    _arg_list = (
        (
            ('-d', '--dir'),
            {'help': 'Location for ControlBeast repository (defaults to current work directory)', 'action': 'store'}
        ),
    )

    def handle(self):
        """
        Command handler for the init command
        """
        if 'dir' in self._args and self._args.dir:
            path = self._args.dir
        else:
            path = os.path.abspath(os.getcwd())

        self._status = os.EX_OK

        try:
            scm_init(path)
        except CbSCMBinaryError as bin_err:
            print(bin_err)
            self._status = os.EX_OSFILE
        except CbSCMInitError as ini_err:
            print(ini_err)
            self._status = os.EX_IOERR
