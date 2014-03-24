# -*- coding: utf-8 -*-
"""
    controlbeast.cli.add
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
import os
from controlbeast import get_conf
import controlbeast.cli.base
from controlbeast.scm import scm_get_root, CbSCMRepoError


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

        # Check which repository to use
        try:
            repository = scm_get_root(path=path)
        except CbSCMRepoError as err:
            return self._terminate(err, os.EX_IOERR)

        # Test if host identifier already in use
        if os.path.isdir(os.path.join(repository, get_conf('dir.repo.hosts'), name)):
            return self._terminate('Identifier {id} already in use.'.format(id=name), os.EX_DATAERR)

        # Create directory structure for new host
        os.makedirs(os.path.join(repository, get_conf('dir.repo.hosts'), name))
        os.makedirs(os.path.join(repository, get_conf('dir.repo.hosts'), name, get_conf('dir.host.base')))
        os.makedirs(os.path.join(repository, get_conf('dir.repo.hosts'), name, get_conf('dir.host.jails')))
        os.makedirs(os.path.join(repository, get_conf('dir.repo.hosts'), name, get_conf('dir.host.conf.auto')))
        os.makedirs(os.path.join(repository, get_conf('dir.repo.hosts'), name, get_conf('dir.host.conf.custom')))

        self._status = os.EX_OK