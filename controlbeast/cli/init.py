# -*- coding: utf-8 -*-
"""
    controlbeast.cli.init
    ~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
import getpass
import os
import controlbeast.cli.base
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

        print('''
Your newly created ControlBeast repository will probably contain some sensitive
information (such as identification tokens, passwords etc.) that are best kept
secret. You may now enter a password which will be used to encrypt this kind of
information.

WARNING: leaving the password empty will entail unencrypted storage of
         potentially sensitive information!
''')

        # Try getting a password. If nothing is entered or verification fails three times,
        # do not enable encryption for the key store.
        password = ''
        verify = ''
        password = getpass.getpass()
        count = 0
        if password:
            while verify != password:
                verify = getpass.getpass(prompt='Verify password: ')
                count += 1
                if count >= 3:
                    print('Unable to verify password, will continue with encryption turned off.')
                    break

        # create basic directory structure
        # TODO: complete implementation of handle method

        # commit the changes
        try:
            scm_commit(path=path, message="Repository initialisation")
        except CbSCMBinaryError as bin_err:
            return self._terminate(bin_err, os.EX_OSFILE)
        except CbSCMCommitError as ini_err:
            return self._terminate(ini_err, os.EX_IOERR)
