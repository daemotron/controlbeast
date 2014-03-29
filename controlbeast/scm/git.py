# -*- coding: utf-8 -*-
"""
    controlbeast.scm.git
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
import os
import re
from controlbeast.scm.base import CbSCMWrapper, CbSCMInitError, CbSCMCommitError, CbSCMRepoError, CbSCMBranchError, \
    CbSCMCheckoutError


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

    def create_branch(self, *args, **kwargs):
        """
        Create a branch within a git repository.

        :param str path:    Path on the file system where the repository resides. If not specified, it defaults to the
                            current work directory.
        :param str name:    Name of the branch to be created.
        """
        path = None
        name = ""

        if len(args) > 0:
            path = args[0]

        if len(args) > 2:
            name = args[1]

        if 'path' in kwargs:
            path = kwargs['path']

        if 'name' in kwargs:
            name = kwargs['name']

        if not path:
            path = os.path.abspath(os.getcwd())

        if not name:
            raise CbSCMBranchError(path=path, branch=name, text='No branch name specified')

        if name in self.get_branches(path=path):
            raise CbSCMBranchError(path=path, branch=name, text='Branch name specified already exists')

        # Git can only operate in the current work directory, so we have to change the current working
        # directory to the path of the repository we are expected to create the branch on.
        current_dir = os.path.abspath(os.getcwd())
        os.chdir(path)

        self._run(['branch', '--quiet', name], path, CbSCMBranchError)
        if self._return_code != os.EX_OK:
            raise CbSCMBranchError(path=path, branch=name, text=self.stderr)

        # Switch back to the previous working directory
        os.chdir(current_dir)

    def get_branches(self, *args, **kwargs):
        """
        Get a list of branches existing with in the repository.

        :param str path:    Path on the file system where the repository resides. If not specified, it defaults to the
                            current work directory.
        :return:            list of branch names
        :rtype:             list
        """
        path = None

        if len(args) > 0:
            path = args[0]

        if 'path' in kwargs:
            path = kwargs['path']

        if not path:
            path = os.path.abspath(os.getcwd())

        # Git can only operate in the current work directory, so we have to change the current working
        # directory to the path of the repository we are expected to get the list of branches from.
        current_dir = os.path.abspath(os.getcwd())
        os.chdir(path)

        self._run(['branch', '--list', '--no-color', '--no-column'], path, CbSCMRepoError)
        if self._return_code != os.EX_OK:
            raise CbSCMRepoError(scm_name=self._binary_name, path=path, text=self.stderr)

        # Switch back to the previous working directory
        os.chdir(current_dir)

        pattern = re.compile(r'^\s*\**\s+')
        return [pattern.sub('', candidate) for candidate in self.stdout.splitlines(keepends=False)]

    def checkout(self, *args, **kwargs):
        """
        Check out a branch within a git repository.

        :param str path:    Path on the file system where the repository resides. If not specified, it defaults to the
                            current work directory.
        :param str name:    Name of the branch to be checked out.
        """
        path = None
        name = ""

        if len(args) > 0:
            path = args[0]

        if len(args) > 2:
            name = args[1]

        if 'path' in kwargs:
            path = kwargs['path']

        if 'name' in kwargs:
            name = kwargs['name']

        if not path:
            path = os.path.abspath(os.getcwd())

        if not name:
            raise CbSCMCheckoutError(path=path, branch=name, text='No branch name specified.')

        if name not in self.get_branches(path=path):
            raise CbSCMCheckoutError(path=path, branch=name, text='Branch name specified does not exist.')

        # Git can only operate in the current work directory, so we have to change the current working
        # directory to the path of the repository we are expected to execute the checkout on.
        current_dir = os.path.abspath(os.getcwd())
        os.chdir(path)

        self._run(['checkout', '-q', name], path, CbSCMCheckoutError)
        if self._return_code != os.EX_OK:
            raise CbSCMCheckoutError(path=path, branch=name, text=self.stderr)

        # Switch back to the previous working directory
        os.chdir(current_dir)

    def get_active_branch(self, *args, **kwargs):
        """
        Get the active named branch of an existing git repository.

        :param str path:    Path on the file system where the repository resides. If not specified, it defaults to the
                            current work directory.
        :return:            Name of the active branch
        :rtype:             str
        """
        path = None

        if len(args) > 0:
            path = args[0]

        if 'path' in kwargs:
            path = kwargs['path']

        if not path:
            path = os.path.abspath(os.getcwd())

        # Git can only operate in the current work directory, so we have to change the current working
        # directory to the path of the repository we are expected to detect the active branch on.
        current_dir = os.path.abspath(os.getcwd())
        os.chdir(path)

        self._run(['branch', '--list', '--no-color', '--no-column'], path, CbSCMRepoError)
        if self._return_code != os.EX_OK:
            raise CbSCMRepoError(scm_name=self._binary_name, path=path, text=self.stderr)

        # Switch back to the previous working directory
        os.chdir(current_dir)

        pattern = re.compile(r'\s*\*+\s+(\S+)')
        return pattern.search(self.stdout).groups()[0]

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
