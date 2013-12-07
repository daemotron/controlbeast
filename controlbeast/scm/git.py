# -*- coding: utf-8 -*-
"""
    controlbeast.scm.git
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
import os

from controlbeast.scm.base import CbSCMWrapper, CbSCMInitError, CbSCMCommitError


class Git(CbSCMWrapper):
    """
    Class acting as wrapper for the git command line interface
    """

    _scm_binary_name = 'git'

    def init(self, *args, **kwargs):
        """
        Initialise a git repository.

        :param str path: Path on the file system where the repository should reside. If not specified, it defaults to the
                         current work directory.
        """
        path = None

        if len(args) > 0:
            path = args[0]

        if 'path' in kwargs:
            path = kwargs['path']

        if not path:
            path = os.path.abspath(os.getcwd())

        self._execute([self._scm_binary_path, 'init', path], path, CbSCMInitError)

    def commit(self, *args, **kwargs):
        """
        Commit to a git repository.

        :param str path:    Path on the file system where the repository resides. If not specified, it defaults to the
                            current work directory.
        :param str message: Commit message to be attached to the commit record.
        """
        path = None
        message = ""

        if len(args) > 0:
            path = args[0]

        if len(args) > 2:
            message = args[1]

        if 'path' in kwargs:
            path = kwargs['path']

        if 'message' in kwargs:
            message = kwargs['message']

        if not path:
            path = os.path.abspath(os.getcwd())

        # Git can only commit in the current work directory, so we have to change the current working
        # directory to the path of the repository we are expected to execute the commit on.
        current_dir = os.path.abspath(os.getcwd())
        os.chdir(path)

        # Before committing to git, changes have to be staged for the commit process
        self._execute([self._scm_binary_path, 'add', '.'], path, CbSCMCommitError)
        self._execute([self._scm_binary_path, 'commit', '-a', '-m', message], path, CbSCMCommitError)

        # Switch back to the previous working directory
        os.chdir(current_dir)
