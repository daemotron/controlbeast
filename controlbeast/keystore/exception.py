# -*- coding: utf-8 -*-
"""
    controlbeast.keystore.exception
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
from controlbeast.utils.dynamic import CbDynamic


class CbKsError(CbDynamic, Exception):
    """
    Basic Key Store exception class
    """
    def __init__(self, *args, **kwargs):
        """
        Basic SSH Exception constructor

        :param list args:   list of positional arguments, will be ignored
        :param dict kwargs: keyword arguments, will be converted into Exception properties
        """
        self._filename = ''
        super().__init__(*args, **kwargs)


class CbKsPasswordError(CbKsError):
    """
    Key Store password error.

    This exception is raised when an encrypted key store is accessed using the wrong passphrase
    """
    def __str__(self):
        if self._filename:
            return "Invalid password for accessing key store at {file}.".format(file=self._filename)
        else:
            return "Invalid password for accessing key store."


class CbKsIOError(CbKsError):
    """
    Key Store I/O error.

    This exception is raised when a key store file cannot be accessed.
    """
    def __str__(self):
        if self._filename:
            return "Insufficient privileges for accessing key store at {file}.".format(file=self._filename)
        else:
            return "Insufficient privileges for accessing key store."