# -*- coding: utf-8 -*-
"""
    controlbeast.scm.base
    ~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
import os
import subprocess
from controlbeast.utils.dynamic import CbDynamic


class CbSCMError(CbDynamic, Exception):
    """
    Basic SCM Exception class
    """
    def __init__(self, *args, **kwargs):
        """
        """
        self._path = ""
        self._text = ""
        self._scm_name = ""
        super().__init__(*args, **kwargs)


class CbSCMBinaryError(CbSCMError):
    """
    SCM Binary Error

    This exception is raised when the expected scm binary cannot be found or is not accessible.
    """
    def __str__(self):
        if self._scm_name:
            return "{scm} is not available on your computer.".format(scm=self._scm_name)
        else:
            return "Expected SCM is not available on your computer."


class CbSCMInitError(CbSCMError):
    """
    SCM Initialisation Error

    This exception is raised when the initialisation of a SCM repository failed.
    """
    def __str__(self):
        if self._text:
            return "Initialisation of {path} failed:\n{text}".format(path=self._path, text=self._text)
        else:
            return "Initialisation of {path} failed for unknown reason".format(path=self._path)


class CbSCMCommitError(CbSCMError):
    """
    SCM Commit Error

    This exception is raised when the commit to a SCM repository failed.
    """
    def __str__(self):
        if self._text:
            return "Commit to {path} failed:\n{text}".format(path=self._path, text=self._text)
        else:
            return "Commit to {path} failed for unknown reason.".format(path=self._path)


class CbSCMWrapper(object):
    """
    The class from which all SCM interface wrappers derive
    """

    _scm_binary_name = None
    _scm_binary_path = None

    def __init__(self):
        """
        The CbSCMWrapper constructor
        """
        self.detect_binary()

    def _execute(self, arguments, path, exception):
        """
        Run the command described by arguments and catch eventual exceptions.

        :param arguments: list of arguments as expected by the various :py:mod:`subprocess` functions
        :param exception: reference to the exception class to be raised if anything goes wrong
        :return: stdout and stderr captures from the process execution
        :rtype: tuple of strings
        """
        #noinspection PyUnusedLocal
        err = out = ""
        process = subprocess.Popen(arguments, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        try:
            out, err = process.communicate()
        except subprocess.CalledProcessError:
            raise exception(scm_name=self._scm_binary_name, path=path, text=err)
        except (OSError, FileNotFoundError):
            raise CbSCMBinaryError(scm_name=self._scm_binary_name)
        # Popen.communicate usually does not raise an exception, so we have to catch this manually:
        if err:
            raise exception(scm_name=self._scm_binary_name, path=path, text=err)
        return out, err

    def detect_binary(self):
        """
        Look for the scm binary and store its path in _scm_binary_path
        """
        # only act if _scm_binary_name has been defined
        if self._scm_binary_name:
            for path in os.get_exec_path():
                binary = os.path.join(path, self._scm_binary_name)
                # perform test on effective [g,u]uid on platforms supporting this in order to
                # grant respecting an eventually set SUID bit
                if os.access in os.supports_effective_ids:
                    status = os.access(binary, os.X_OK, effective_ids=True)
                else:
                    status = os.access(binary, os.X_OK, effective_ids=False)

                if status:
                    self._scm_binary_path = binary
                    break
        if not self._scm_binary_path:
            raise CbSCMBinaryError(self._scm_binary_name)

    def init(self, *args, **kwargs):
        """
        The init method contains the actual code for the repository initialisation.
        This method needs to be implemented for each SCM wrapper class
        """
        raise NotImplementedError

    def commit(self, *args, **kwargs):
        """
        The commit method contains the actual code for committing updated content into
        the repository. This method needs to be implemented for each SCM wrapper class
        """
        raise NotImplementedError