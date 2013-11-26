# -*- coding: utf-8 -*-
"""
    controlbeast.scm.git
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
import os
import subprocess

from controlbeast.scm.base import CbSCMWrapper, CbSCMBinaryError, CbSCMInitError


class Git(CbSCMWrapper):
    """
    Class acting as wrapper for the git command line interface
    """

    _scm_binary_name = 'git'

    def init(self, *args, **kwargs):
        """
        Initialise a git repository.

        :param path: Path on the file system where the repository should reside. If not specified, it defaults to the
                     current work directory.
        """
        path = None

        if len(args) > 0:
            path = args[0]

        if 'path' in kwargs:
            path = kwargs['path']

        if not path:
            path = os.path.abspath(os.getcwd())

        process = subprocess.Popen(
            [self._scm_binary_path, 'init', path], stderr=subprocess.PIPE, stdout=subprocess.PIPE
        )
        #noinspection PyUnusedLocal
        out = err = ""
        try:
            out, err = process.communicate()
        except subprocess.CalledProcessError:
            raise CbSCMInitError(path, err)
        except (OSError, FileNotFoundError):
            raise CbSCMBinaryError(self._scm_binary_name)

        # Popen.communicate usually does not raise an exception, so we have to catch this case manually
        if err:
            raise CbSCMInitError(path, err.decode(errors='replace'))