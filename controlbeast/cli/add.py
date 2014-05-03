# -*- coding: utf-8 -*-
"""
    controlbeast.cli.add
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
import os
import controlbeast.cli.base
from controlbeast.conf import get_conf
from controlbeast.scm import scm_get_root, CbSCMRepoError, scm_get_branches, scm_checkout, scm_create_branch


class AddCommand(controlbeast.cli.base.CbCommand):
    """
    Command class implementing the add command
    """

    _help = 'Add a new host to the ControlBeast repository'
    _arg_list = (
        (
            ('-d', '--dir'),
            {'help': 'Location for ControlBeast repository (defaults to current work directory)', 'action': 'store'}
        ),
        (
            ('-n', '--name'),
            {'help': 'Identifier of the host to be added to the repository', 'action': 'store'}
        ),
        (
            ('-s', '--source'),
            {
                'help': 'Source branch for the host to be created from. Defaults to {}.'.format(get_conf('SCM_BRANCH')),
                'default': get_conf('SCM_BRANCH'),
                'action': 'store'
            }
        )
    )

    def handle(self):
        """
        Command handler for the add command
        """
        # get path to operate on/from, either from arguments or from CWD
        if 'dir' in self._args and self._args.dir:
            path = self._args.dir
        else:
            path = os.path.abspath(os.getcwd())

        # get identifier, either form arguments or from direct input
        if 'name' in self._args and self._args.name:
            name = self._args.name
        else:
            name = ''
            while name == '':
                name = input('Please enter an identifier for the host:\n>> ')

        # get source branch from arguments or from default
        if 'source' in self._args and self._args.source:
            source = self._args.source
        else:
            source = get_conf('SCM_BRANCH')

        # Check which repository to use
        try:
            repository = scm_get_root(path=path)
        except CbSCMRepoError as err:
            return self._terminate(err, os.EX_IOERR)

        # Test if host identifier already in use
        if name in scm_get_branches(path=path):
            return self._terminate(
                'Host identifier must be unique. `{host}` is already in use.\n'.format(host=name),
                os.EX_DATAERR
            )

        # Test if selected source branch exists
        if not source in scm_get_branches(path=path):
            return self._terminate('The selected source branch `{}` does not exist.\n'.format(source), os.EX_DATAERR)

        # Switch to source branch, create host branch from it and activate it
        scm_checkout(path=path, name=source)
        scm_create_branch(path=path, name=name)
        scm_checkout(path=path, name=name)

        self._status = os.EX_OK
