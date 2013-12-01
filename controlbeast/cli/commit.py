# -*- coding: utf-8 -*-
"""
    controlbeast.cli.commit
    ~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
import os

import controlbeast.cli.base
from controlbeast.scm import scm_commit, CbSCMBinaryError, CbSCMCommitError


class CommitCommand(controlbeast.cli.base.CbCommand):
    """
    Command class implementing the init command
    """

    _help = 'Commit to ControlBeast repository'
    _arg_list = (
        (
            ('-d', '--dir'),
            {'help': 'Location of ControlBeast repository (defaults to current work directory)', 'action': 'store'}
        ),
        (
            ('-m,', '--message'),
            {'help': 'Commit message to be attached to the current commit', 'action': 'store'}
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

        if 'message' in self._args and self._args.message:
            message = self._args.message
        else:
            message = ''
            while message == '':
                message = input("Please enter a commit message:\n>> ")

        self._status = os.EX_OK

        try:
            scm_commit(path=path, message=message)
        except CbSCMBinaryError as bin_err:
            print(bin_err)
            self._status = os.EX_OSFILE
        except CbSCMCommitError as ini_err:
            print(ini_err)
            self._status = os.EX_IOERR
