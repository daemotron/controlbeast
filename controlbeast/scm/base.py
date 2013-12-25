# -*- coding: utf-8 -*-
"""
    controlbeast.scm.base
    ~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
import subprocess
from controlbeast.utils.binary import CbBinary
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


class CbSCMRepoError(CbSCMError):
    """
    SCM Repository Error

    This exception is raised when the repository is not valid, damaged or does not exist.
    """
    def __str__(self):
        if self._text:
            return "Repository at {path} is not valid:\n{text}".format(path=self._path, text=self._text)
        else:
            return "Repository at {path} is not valid.".format(path=self._path)


class CbSCMWrapper(CbBinary):
    """
    The class from which all SCM interface wrappers derive
    """

    def __init__(self, binary_name=''):
        super(CbSCMWrapper, self).__init__(binary_name=binary_name)
        if not self._binary_path:
            raise CbSCMBinaryError(self._binary_name)
        self._arguments = []

    def _run(self, arguments, path, exception):
        """
        Run the command described by arguments and catch eventual exceptions.

        :param list arguments: list of arguments as expected by the various :py:mod:`subprocess` functions, excluding
                               the path to the binary (cf. :py:class:`~controlbeast.utils.binary.CbBinary`)
        :param str path:       file system path representing the location of the SCM repository
        :param exception:      reference to the exception class to be raised if anything goes wrong
        """
        self._arguments = arguments
        try:
            self._execute()
        except subprocess.CalledProcessError:
            raise exception(scm_name=self._binary_name, path=path, text=self.stderr)
        except (OSError, FileNotFoundError):
            raise CbSCMBinaryError(scm_name=self._binary_name)

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

    def get_root(self, *args, **kwargs):
        """
        Get the path to the root of the SCM repository
        """
        raise NotImplementedError
