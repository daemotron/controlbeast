# -*- coding: utf-8 -*-
"""
    controlbeast.ssh.result
    ~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""


from controlbeast.ssh.api import CbSSHLib, SSH_OK
from controlbeast.ssh.exception import CbSSHCommunicationError, CbSSHExecutionError
from controlbeast.utils.convert import to_bytes, to_str


class CbSSHLazyResult(object):
    """
    Class acting as lazy, iterable command execution result wrapper.

    When the first iteration starts, the command will actually be executed on the remote system.
    With each iteration, a further chunk of output data is read from the connection to the remote
    host and returned as byte sequence.

    .. note::

       For the iteration to work, it is crucial that the :py:class:`~controlbeast.ssh.session.CbSSHSession` object
       remains intact. De-referencing this object or destroying it by any other means will entail immediate
       shutdown of the SSH connection, rendering any further output gathering from this connection impossible.

    :param str hostname: host name or ip address of the remote system
    :param session: libssh session object with active connection
    :param str command: command string to be executed on the remote system
    """

    #: string representing the remote host's ip address or hostname
    _hostname = ''

    #: return code resulting from the remote command execution
    _return_code = None

    #: flag signalizing that the result is already consumed
    _iteration_flag = False

    #: flag signalizing that the result iteration has reached its end
    _next_flag = False

    #: local reference to libssh API instance
    _libssh = None

    #: libssh session object
    _session = None

    #: libssh channel object
    _channel = None

    def __init__(self, hostname, session, command):
        """
        Result constructor
        """
        self._hostname = to_str(hostname)
        self._session = session
        self._command = to_bytes(command)
        self._libssh = CbSSHLib.get_instance()

    def __next__(self):
        if self._next_flag:
            raise StopIteration()

        # Read data from the ssh communication channel
        data = self._libssh.ssh_channel_read(self._channel, 10)
        if data:
            return data

        # No more data received ==> clean up and stop iteration
        self._libssh.ssh_channel_send_eof(self._channel)
        self._return_code = self._libssh.ssh_channel_get_exit_status(self._channel)
        self._libssh.ssh_channel_free(self._channel)
        self._channel = None
        self._next_flag = True
        raise StopIteration()

    def __iter__(self):
        if self._iteration_flag:
            raise RuntimeError("Result is already consumed.")

        self._iteration_flag = True
        self._next_flag = False

        # Open the communication channel
        self._channel = self._libssh.ssh_channel_new(self._session)
        return_code = self._libssh.ssh_channel_open_session(self._channel)
        if return_code != SSH_OK:
            raise CbSSHCommunicationError(return_code=return_code, hostname=self._hostname)

        # Execute the command
        return_code = self._libssh.ssh_channel_request_exec(self._channel, self._command)
        if return_code != SSH_OK:
            raise CbSSHExecutionError(
                hostname=self._hostname,
                return_code=return_code,
                message=to_str(self._libssh.get_error(self._session)),
                command=to_str(self._command)
            )

        return self

    def as_bytes(self):
        """
        Launch the command execution and return the result as byte sequence.

        :return: byte sequence representing command execution result
        :rtype: :class:`bytes`
        """
        return b''.join([x for x in self])

    def as_str(self):
        """
        Launch the command execution and return the result as string.

        :return: string representing command execution result
        :rtype: :class:`str`
        """
        return to_str(self.as_bytes())

    def wait(self):
        """
        Wait until remote command execution has completed.

        :return: remote return code
        :rtype: :class:`int`
        """
        list(self)
        return self.return_code

    @property
    def return_code(self):
        """
        Return code of the remote command execution
        """
        return self._return_code


class CbSSHResult(CbSSHLazyResult):
    """
    Class acting as non-iterable SSH command execution result wrapper.

    Other than :py:class:`~controlbeast.ssh.result.CbSSHLazyResult`, the command is
    immediately executed and returned data are cached. This behaviour is usually more
    convenient when executing simple commands with small amounts of return data.
    """

    #: data returned from command execution
    _data = None

    def __init__(self, *args, **kwargs):
        super(CbSSHResult, self).__init__(*args, **kwargs)

        # iterate and save state
        self._data = list(self)

    def as_bytes(self):
        """
        Return command execution result as byte sequence from cache

        :return: byte sequence representing command execution result
        :rtype: :class:`bytes`
        """
        return b''.join(self._data)

    def wait(self):
        """
        Override wait method to avoid raising an error due to repeatedly trying to iterate
        """
        return self.return_code