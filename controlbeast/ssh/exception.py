# -*- coding: utf-8 -*-
"""
    controlbeast.ssh.exception
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""

from controlbeast.utils.dynamic import CbDynamic


class CbSSHError(CbDynamic, Exception):
    """
    Basic SSH Exception class
    """
    def __init__(self, *args, **kwargs):
        """
        Basic SSH Exception constructor

        :param list args:   list of positional arguments, will be ignored
        :param dict kwargs: keyword arguments, will be converted into Exception properties
        """
        self._hostname = ''
        self._port = ''
        self._username = ''
        self._library = ''
        self._return_code = 0
        self._message = ''
        self._command = ''
        super().__init__(*args, **kwargs)


class CbSSHLibraryError(CbSSHError):
    """
    SSH Library Error

    This exception is raised when the expected library is incompatible, cannot be found or is not accessible.
    """
    def __str__(self):
        if self._library:
            return "{library} is not available or incompatible on your computer".format(library=self._library)
        else:
            return "libssh is not available or incompatible on your computer."


class CbSSHConnectionError(CbSSHError):
    """
    SSH Connection Error

    This exception is raised when the connection to a remote host cannot be established.
    """
    def __str__(self):
        return "Connection to {hostname}:{port} failed: Error {error}: {message}".format(
            hostname=self._hostname,
            port=self._port,
            error=self._return_code,
            message=self._message
        )


class CbSSHAuthenticationError(CbSSHError):
    """
    SSH Authentication Error

    This exception is raised when the authentication on an established connection fails.
    """
    def __str__(self):
        return "Authentication to {hostname} as {username} failed.".format(
            hostname=self._hostname,
            username=self._username
        )


class CbSSHCommunicationError(CbSSHError):
    """
    SSH Communication Error

    This exception is raised when the communication on an established connection fails.
    """
    def __str__(self):
        return "Communication to {hostname} failed. Error code: {code}".format(
            hostname=self._hostname,
            code=self._return_code
        )

class CbSSHExecutionError(CbSSHError):
    """
    SSH Execution Error

    This exception is raised when the remote execution of a command fails.
    """
    def __str__(self):
        return "Remote execution of command on {hostname} failed: Error {error}: {message}\nCommand: {command}".format(
            hostname=self._hostname,
            error=self._return_code,
            message=self._message,
            command=self._command
        )