# -*- coding: utf-8 -*-
"""
    controlbeast.ssh.session
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""


from controlbeast.ssh.exception import CbSSHConnectionError, CbSSHAuthenticationError
from controlbeast.ssh.result import CbSSHLazyResult, CbSSHResult
from controlbeast.utils.convert import to_bytes, to_str
from controlbeast.ssh.api import CbSSHLib, SSH_OK, SSH_AUTH_SUCCESS


class CbSSHSession(object):
    """
    Class acting as SSH session wrapper. The SSH Session Object transparently handles
    connection management, so no explicit ``connect()`` or ``disconnect()`` methods
    exist. As soon as a command execution is requested, the connection to the remote
    host will be established. When an SSH session object gets de-referenced, its connection
    will be closed and the session context will be cleaned up.

    .. warning::

       The :py:class:`~controlbeast.ssh.result.CbSSHLazyResult` relies on the SSH Session Object to persist as long
       as iterating over the result has not been completed. Once the session object gets de-referenced and therefore
       the underlying SSH connection gets closed, trying to iterate further over the result will provoke a
       :py:exc:`~controlbeast.ssh.exception.CbSSHCommunicationError` exception.

    :param str hostname: remote ip address or hostname
    :param str port: remote SSH port
    :param str username: remote username to be used for authentication
    :param str password: remote user's password
    :param str passphrase: passphrase for accessing a (local) private key for authentication
    :param str private_key_file: path to the private key file to be used for authentication
    """

    #: byte sequence representing the remote host's ip address or hostname
    _hostname = b''

    #: byte sequence representing the remote port
    _port = b''

    #: byte sequence representing the remote username used for authentication
    _username = b''

    #: byte sequence representing the remote user's password (only applicable if no pubkey authentication is used)
    _password = b''

    #: byte sequence representing the passphrase for accessing a (local) private key for authentication
    _passphrase = b''

    #: byte sequence representing the path to the private key file to be used for authentication
    _private_key_file = b''

    #: boolean connection status (True = connected, False = disconnected)
    _connection_status = False

    #: boolean session status (True = session exists, False = session destroyed)
    _session_status = False

    #: local reference to libssh API instance
    _libssh = None

    #: libssh session object
    _session = None

    def __init__(self, hostname='localhost', port='22', username='', password='', passphrase='', private_key_file=''):
        """
        Construct an SSH session object.
        """
        self._hostname = to_bytes(hostname)
        self._port = to_bytes(port)
        self._username = to_bytes(username)
        self._password = to_bytes(password)
        self._passphrase = to_bytes(passphrase)
        self._private_key_file = to_bytes(private_key_file)
        self._libssh = CbSSHLib.get_instance()
        self._session_init()

    def execute(self, command, lazy=False):
        """
        Execute the command on the remote host.

        :param str command: command string
        :param bool lazy: set to True for receiving a lazy result object. Useful for commands with large output data
        :return: result instance
        :rtype: :py:class:`~controlbeast.ssh.result.CbSSHResult` or :py:class:`~controlbeast.ssh.result.CbSSHLazyResult`
        """
        if not self._connection_status:
            self._connect()

        if lazy:
            return CbSSHLazyResult(hostname=self.hostname, session=self._session, command=command)
        else:
            return CbSSHResult(hostname=self.hostname, session=self._session, command=command)

    @property
    def hostname(self):
        """
        Remote host's IP address or hostname
        """
        return to_str(self._hostname)

    @property
    def is_connected(self):
        """
        Connection status of the session
        """
        return self._connection_status

    @property
    def keyfile(self):
        """
        Private key file to be used for authentication
        """
        return to_str(self._private_key_file)

    @property
    def port(self):
        """
        Remote SSH port
        """
        return to_str(self._port)

    @property
    def username(self):
        """
        Remote username used for authentication
        """
        return to_str(self._username)

    def _connect(self):
        """
        Open an SSH connection
        """
        if self._connection_status:
            return

        if not self._session_status:
            self._session_init()

        return_code = self._libssh.ssh_connect(self._session)
        if return_code != SSH_OK:
            raise CbSSHConnectionError(
                hostname=self.hostname,
                port=self.port,
                return_code=return_code,
                message=to_str(self._libssh.get_error(self._session))
            )
        self._connection_status = True

        # try public key authentication first
        return_code = self._libssh.ssh_auth_pubkey(self._session, self._passphrase)
        if return_code != SSH_AUTH_SUCCESS:
            # try password authentication next
            return_code = self._libssh.ssh_auth_password(self._session, self._password)
            if return_code != SSH_AUTH_SUCCESS:
                self._disconnect()
                raise CbSSHAuthenticationError(hostname=self.hostname, username=self.username)

    def _reconnect(self):
        """
        Disconnects and reconnects the session
        """
        self._terminate()
        self._session_init()
        self._connect()

    def _session_init(self):
        """
        (Re-)Initialise the libssh session object
        """
        if self._session_status:
            self._terminate()
        self._session = self._libssh.ssh_new()
        self._session_status = True
        if self._username:
            self._libssh.set_username(self._session, self._username)
        self._libssh.set_hostname(self._session, self._hostname)
        self._libssh.set_port(self._session, self._port)
        if self._private_key_file:
            self._libssh.set_private_keyfile(self._session, self._private_key_file)

    def _terminate(self):
        """
        Close initialised ssh connection and clean up session.

        This method is automatically called when a :py:class:`~controlbeast.ssh.session.CbSSHSession` object is
        de-referenced, so it does not need to be called explicitly.
        """
        if self._connection_status:
            self._libssh.ssh_disconnect(self._session)
        self._connection_status = False
        if self._session_status:
            self._libssh.ssh_free(self._session)
        self._session_status = False

    _disconnect = _terminate

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._terminate()

