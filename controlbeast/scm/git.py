# -*- coding: utf-8 -*-
"""
    controlbeast.scm.git
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
import os
from controlbeast.scm.base import CbSCMWrapper, CbSCMInitError, CbSCMCommitError, CbSCMRepoError


class Git(CbSCMWrapper):
    """
    Class acting as wrapper for the git command line interface
    """

    def __init__(self):
        super(Git, self).__init__(binary_name='git')
        self._arguments = []

    def init(self, *args, **kwargs):
        """
        Initialise a git repository.

        :param str path: Path on the file system where the repository should reside. If not specified, it defaults to
                         the current work directory.
        """
        path = None

        if len(args) > 0:
            path = args[0]

        if 'path' in kwargs:
            path = kwargs['path']

        if not path:
            path = os.path.abspath(os.getcwd())

        self._run(['init', path], path, CbSCMInitError)
        if self.return_code != os.EX_OK:
            raise CbSCMInitError(scm_name=self._binary_name, path=path, text=self.stderr)

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
        self._run(['add', '.'], path, CbSCMCommitError)
        if self.return_code != os.EX_OK:
            raise CbSCMCommitError(scm_name=self._binary_name, path=path, text=self.stderr)
        self._run(['commit', '-a', '-m', message], path, CbSCMCommitError)
        if self.return_code != os.EX_OK:
            raise CbSCMCommitError(scm_name=self._binary_name, path=path, text=self.stderr)

        # Switch back to the previous working directory
        os.chdir(current_dir)

    def get_root(self, *args, **kwargs):
        """
        Get the path to the root of a git repository.

        :param str path: Path on the file system where to start looking for the repository's root directory
        """
        path = None

        if len(args) > 0:
            path = args[0]

        if 'path' in kwargs:
            path = kwargs['path']

        if not path:
            path = os.path.abspath(os.getcwd())

        # Git can only commit in the current work directory, so we have to change the current working
        # directory to the path of the repository we are expected to execute the commit on.
        current_dir = os.path.abspath(os.getcwd())
        os.chdir(path)

        self._run(['rev-parse', '--show-toplevel'], path, CbSCMRepoError)
        if self.return_code != os.EX_OK:
            raise CbSCMRepoError(scm_name=self._binary_name, path=path, text=self.stderr)

        # Switch back to the previous working directory
        os.chdir(current_dir)
        return self.stdout.strip()
