# -*- coding: utf-8 -*-
"""
    controlbeast.scm.base
    ~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
import os


class CbSCMError(Exception):
    """
    Basic SCM Exception class
    """
    pass


class CbSCMBinaryError(CbSCMError):
    """
    SCM Binary Error

    This exception is raised when the expected scm binary cannot be found or is not accessible.
    """
    def __init__(self, scm_name):
        self._scm_name = scm_name

    def __str__(self):
        return "{scm} is not available on your computer.".format(scm=self._scm_name)


class CbSCMInitError(CbSCMError):
    """
    SCM Initialisation Error

    This exception is raised when the initialisation of a SCM repository failed.
    """
    def __init__(self, path, text):
        self._path = path
        self._text = text

    def __str__(self):
        if self._text:
            return "Initialisation of {path} failed:\n{text}".format(path=self._path, text=self._text)
        else:
            return "Initialisation of {path} failed for unknown reason".format(path=self._path)


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