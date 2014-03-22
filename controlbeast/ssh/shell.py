# -*- coding: utf-8 -*-
"""
    controlbeast.ssh.shell
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""


import time
from controlbeast.ssh.exception import CbSSHConnectionError
from controlbeast.ssh.session import CbSSHSession
from controlbeast.ssh.api import SSH_OK
from controlbeast.utils.convert import to_str, to_bytes


class CbSSHShell(CbSSHSession):
    """
    Class providing an interactive SSH Shell session. Connection management is handled
    transparently, so no explicit ``connect()`` or ``disconnect()`` methods exist. As
    soon as one tries reading or writing to the shell session, the connection to the
    remote host will be established. When an SSH shell session object gets de-referenced,
    its connection will be closed and the session context will be cleaned up.

    :param str hostname: remote ip address or hostname
    :param str port: remote SSH port
    :param str username: remote username to be used for authentication
    :param str password: remote user's password
    :param str passphrase: passphrase for accessing a (local) private key for authentication
    :param str private_key_file: path to the private key file to be used for authentication
    """

    #: boolean channel status (True = channel exists, False = channel destroyed)
    _channel_status = False

    #: libssh channel object
    _channel = None

    def __init__(self, hostname='localhost', port='22', username='', password='', passphrase='', private_key_file=''):
        """
        Construct an SSH Shell session object.
        """
        super(CbSSHShell, self).__init__(
            hostname=hostname,
            port=port,
            username=username,
            password=password,
            passphrase=passphrase,
            private_key_file=private_key_file
        )

    def write(self, data):
        """
        Write data to remote shell.

        .. note::

           This method will automatically establish an SSH connection and spawn a remote
           shell, should this not already have happened.

        :param str data: data to be written to remote shell.
        """
        if not self._channel_status:
            self._channel_init()
        bytes_written = self._libssh.ssh_channel_write(self._channel, to_bytes(data))
        if bytes_written != len(data):
            raise RuntimeError("Error writing data to SSH socket.")

    def read(self, max_bytes=0):
        """
        Read data from remote shell. If a limit has been specified, a maximum of ``max_bytes`` bytes will
        be read and returned. Otherwise, all data until EoF will be read and returned.

        .. note::

           This method will automatically establish an SSH connection and spawn a remote
           shell, should this not already have happened.

        :param   int max_bytes: maximum number of bytes to be read from remote shell
        :return: data read from remote connection
        :rtype:  str
        """
        if not self._channel_status:
            self._channel_init()
        if not self._libssh.ssh_channel_is_open(self._channel):
            raise RuntimeError("SSH remote shell seems to be closed.")

        if max_bytes:
            return to_str(self._libssh.ssh_channel_read_nonblocking(self._channel, max_bytes))
        else:
            buffer = ""
            while not self._libssh.ssh_channel_is_eof(self._channel):
                buffer += to_str(self._libssh.ssh_channel_read_nonblocking(self._channel, 80))
            return buffer

    # noinspection PyMethodOverriding
    def execute(self, command):
        """
        Execute the command on the remote host.

        :param   str command: command string
        :return: output from the remote shell
        :rtype:  str
        """
        # empty queue
        buffer = self.read(1024)
        while len(buffer) > 0:
            time.sleep(0.5)
            buffer = self.read(1024)
        # Send command
        self.write("{cmd}\n".format(cmd=command))
        # Retrieve output
        result = ""
        time.sleep(0.5)
        buffer = self.read(1024)
        result += buffer
        while len(buffer) > 0:
            time.sleep(0.5)
            buffer = self.read(1024)
            result += buffer
        return result

    def _do_or_die(self, function, *args, **kwargs):
        """
        Execute function with corresponding arguments. If the function returns anything but
        ``SSH_OK``, an exception is raised.

        :param function:  pointer to function or method to be executed
        :param args:      positional arguments for this function or method
        :param kwargs:    key word arguments for this function or method
        """
        return_code = function(*args, **kwargs)
        if return_code != SSH_OK:
            raise CbSSHConnectionError(
                hostname=self.hostname,
                port=self.port,
                return_code=return_code,
                message=to_str(self._libssh.get_error(self._session))
            )

    def _channel_init(self):
        """
        (Re-)Initialise the libssh channel object
        """
        if not self._connection_status:
            self._connect()
        if self._channel_status:
            self._channel_terminate()
        self._channel = self._libssh.ssh_channel_new(self._session)
        self._do_or_die(self._libssh.ssh_channel_open_session, self._channel)
        self._do_or_die(self._libssh.ssh_channel_request_pty, self._channel)
        self._do_or_die(self._libssh.ssh_channel_request_shell, self._channel)
        self._channel_status = True

    def _channel_terminate(self):
        """
        Close initialised channel and clean up.
        """
        if self._channel_status and self._channel is not None:
            if self._libssh.ssh_channel_is_open(self._channel):
                self._libssh.ssh_channel_close(self._channel)
                self._libssh.ssh_channel_send_eof(self._channel)

            self._libssh.ssh_channel_free(self._channel)
            self._channel = None
        self._channel_status = False

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._channel_terminate()
        super(CbSSHShell, self)._terminate()