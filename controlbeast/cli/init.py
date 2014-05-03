# -*- coding: utf-8 -*-
"""
    controlbeast.cli.init
    ~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
import os
import controlbeast.cli.base
from controlbeast.core.template import CbTemplate
from controlbeast.scm import scm_init, CbSCMBinaryError, CbSCMInitError, scm_commit, CbSCMCommitError


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

        # initialise an empty repository
        try:
            scm_init(path)
        except CbSCMBinaryError as bin_err:
            return self._terminate(bin_err, os.EX_OSFILE)
        except CbSCMInitError as ini_err:
            return self._terminate(ini_err, os.EX_IOERR)

        # create basic directory structure
        template = CbTemplate('master', path)
        try:
            template.deploy()
        except (RuntimeError, PermissionError) as err:
            return self._terminate(err, os.EX_IOERR)

        # commit the changes
        try:
            scm_commit(path=path, message="Repository initialisation")
        except CbSCMBinaryError as bin_err:
            return self._terminate(bin_err, os.EX_OSFILE)
        except CbSCMCommitError as ini_err:
            return self._terminate(ini_err, os.EX_IOERR)
