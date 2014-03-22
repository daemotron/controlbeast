# -*- coding: utf-8 -*-
"""
    controlbeast.ssh.api
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013, 2014 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""

import ctypes
import ctypes.util
from controlbeast.utils.singleton import CbSingleton
from controlbeast.ssh.exception import CbSSHLibraryError


SSH_OK = 0
SSH_ERROR = -1
SSH_AGAIN = -2
SSH_EOF = -127

SSH_OPTIONS_HOST = 0
SSH_OPTIONS_PORT = 1
SSH_OPTIONS_PORT_STR = 2
SSH_OPTIONS_FD = 3
SSH_OPTIONS_USER = 4
SSH_OPTIONS_SSH_DIR = 5
SSH_OPTIONS_IDENTITY = 6
SSH_OPTIONS_ADD_IDENTITY = 7
SSH_OPTIONS_KNOWNHOSTS = 8
SSH_OPTIONS_TIMEOUT = 9
SSH_OPTIONS_TIMEOUT_USEC = 10
SSH_OPTIONS_SSH1 = 11
SSH_OPTIONS_SSH2 = 12
SSH_OPTIONS_LOG_VERBOSITY = 13
SSH_OPTIONS_LOG_VERBOSITY_STR = 14
SSH_OPTIONS_CIPHERS_C_S = 15
SSH_OPTIONS_CIPHERS_S_C = 16
SSH_OPTIONS_COMPRESSION_C_S = 17
SSH_OPTIONS_COMPRESSION_S_C = 18
SSH_OPTIONS_PROXYCOMMAND = 19
SSH_OPTIONS_BINDADDR = 20
SSH_OPTIONS_STRICTHOSTKEYCHECK = 21
SSH_OPTIONS_COMPRESSION = 22
SSH_OPTIONS_COMPRESSION_LEVEL = 23
SSH_OPTIONS_KEY_EXCHANGE = 24
SSH_OPTIONS_HOSTKEYS = 25
SSH_OPTIONS_GSSAPI_SERVER_IDENTITY = 26
SSH_OPTIONS_GSSAPI_CLIENT_IDENTITY = 27
SSH_OPTIONS_GSSAPI_DELEGATE_CREDENTIALS = 28

SSH_AUTH_SUCCESS = 0
SSH_AUTH_DENIED = 1
SSH_AUTH_PARTIAL = 2
SSH_AUTH_INFO = 3
SSH_AUTH_AGAIN = 4
SSH_AUTH_ERROR = -1


@CbSingleton
class CbSSHLib():
    """
    Class acting as wrapper for the libssh library.

    This wrapper class is implemented following the singleton pattern. Therefore,
    in order to getting a reference to the library, the
    :py:meth:`~controlbeast.utils.singleton.CbSingleton.get_instance` method has to be used.

    Example::

       ssh_lib = CbSSHLib.get_instance()
    """

    #: libssh library reference
    _libssh = None

    class SftpAttributes(ctypes.Structure):
        _fields_ = [("name", ctypes.c_char_p),
                ("longname", ctypes.c_char_p),
                ("flags", ctypes.c_uint32),
                ("type", ctypes.c_uint8),
                ("size", ctypes.c_uint64)]

    def __init__(self):
        library_path = ctypes.util.find_library('ssh')
        if not library_path:
            raise CbSSHLibraryError
        try:
            self._libssh = ctypes.CDLL(library_path)
        except OSError:
            raise CbSSHLibraryError(library=library_path)

        try:
            self._libssh.ssh_new.argtypes = []
            self._libssh.ssh_new.restype = ctypes.c_void_p
            self._libssh.ssh_free.argtypes = [ctypes.c_void_p]
            self._libssh.ssh_connect.argtypes = [ctypes.c_void_p]
            self._libssh.ssh_connect.restype = ctypes.c_int
            self._libssh.ssh_disconnect.argtypes = [ctypes.c_void_p]
            self._libssh.ssh_options_set.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p]
            self._libssh.ssh_userauth_password.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
            self._libssh.ssh_userauth_password.restype = ctypes.c_int
            self._libssh.ssh_userauth_autopubkey.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
            self._libssh.ssh_userauth_autopubkey.restype = ctypes.c_int
            self._libssh.ssh_channel_new.argtypes = [ctypes.c_void_p]
            self._libssh.ssh_channel_new.restype = ctypes.c_void_p
            self._libssh.ssh_channel_open_session.argtypes = [ctypes.c_void_p]
            self._libssh.ssh_channel_open_session.restype = ctypes.c_int
            self._libssh.ssh_channel_request_exec.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
            self._libssh.ssh_channel_request_exec.restype = ctypes.c_int
            self._libssh.ssh_channel_read.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint, ctypes.c_int]
            self._libssh.ssh_channel_read.restype = ctypes.c_int
            self._libssh.ssh_channel_read_nonblocking.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint, ctypes.c_int]
            self._libssh.ssh_channel_read_nonblocking.restype = ctypes.c_int
            self._libssh.ssh_channel_write.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint]
            self._libssh.ssh_channel_write.restype = ctypes.c_int
            self._libssh.ssh_channel_send_eof.argtypes = [ctypes.c_void_p]
            self._libssh.ssh_channel_send_eof.restype = ctypes.c_int
            self._libssh.ssh_channel_is_eof.argtypes = [ctypes.c_void_p]
            self._libssh.ssh_channel_is_eof.restype = ctypes.c_int
            self._libssh.ssh_channel_is_open.argtypes = [ctypes.c_void_p]
            self._libssh.ssh_channel_is_open.restype = ctypes.c_int
            self._libssh.ssh_channel_is_closed.argtypes = [ctypes.c_void_p]
            self._libssh.ssh_channel_is_closed.restype = ctypes.c_int
            self._libssh.ssh_channel_close.argtypes = [ctypes.c_void_p]
            self._libssh.ssh_channel_close.restype = ctypes.c_int
            self._libssh.ssh_channel_free.argtypes = [ctypes.c_void_p]
            self._libssh.ssh_channel_get_exit_status.argtypes = [ctypes.c_void_p]
            self._libssh.ssh_channel_get_exit_status.restype = ctypes.c_int
            self._libssh.ssh_channel_request_env.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
            self._libssh.ssh_channel_request_env.restype = ctypes.c_int
            self._libssh.ssh_channel_request_pty.argtypes = [ctypes.c_void_p]
            self._libssh.ssh_channel_request_pty.restype = ctypes.c_int
            self._libssh.ssh_channel_request_pty_size.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
            self._libssh.ssh_channel_request_pty_size.restype = ctypes.c_int
            self._libssh.ssh_channel_request_shell.argtypes = [ctypes.c_void_p]
            self._libssh.ssh_channel_request_shell.restype = ctypes.c_int
            self._libssh.ssh_get_error.argtypes = [ctypes.c_void_p]
            self._libssh.ssh_get_error.restype = ctypes.c_char_p

            # SFTP
            self._libssh.sftp_new.argtypes = [ctypes.c_void_p]
            self._libssh.sftp_new.restype = ctypes.c_void_p
            self._libssh.sftp_init.argtypes = [ctypes.c_void_p]
            self._libssh.sftp_init.restype = None
            self._libssh.sftp_free.argtypes = [ctypes.c_void_p]
            self._libssh.sftp_fstat.argtypes = [ctypes.c_void_p]
            self._libssh.sftp_fstat.restype = self.SftpAttributes
            self._libssh.sftp_fstat.restype = ctypes.c_void_p
            self._libssh.sftp_open.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
            self._libssh.sftp_open.restype = ctypes.c_void_p
            self._libssh.sftp_close.argtypes = [ctypes.c_void_p]
            self._libssh.sftp_write.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint]
            self._libssh.sftp_write.restype = ctypes.c_int
            self._libssh.sftp_seek64.argtypes = [ctypes.c_void_p, ctypes.c_ulonglong]
            self._libssh.sftp_seek64.restype = ctypes.c_int
            self._libssh.sftp_tell64.argtypes = [ctypes.c_void_p]
            self._libssh.sftp_tell64.restype = ctypes.c_ulonglong
            self._libssh.sftp_read.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint]
            self._libssh.sftp_read.restype = ctypes.c_int

            # Forward
            self._libssh.ssh_channel_open_forward.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
            self._libssh.ssh_channel_open_forward.restype = ctypes.c_int
        except (AttributeError, OSError, IOError):
            raise CbSSHLibraryError(library=library_path)

    def ssh_new(self):
        return self._libssh.ssh_new()

    def ssh_connect(self, session):
        return self._libssh.ssh_connect(session)

    def ssh_auth_pubkey(self, session, passphrase):
        return self._libssh.ssh_userauth_autopubkey(session, passphrase)

    def ssh_auth_password(self, session, password):
        return self._libssh.ssh_userauth_password(session, None, password)

    def ssh_disconnect(self, session):
        self._libssh.ssh_disconnect(session)

    def ssh_free(self, session):
        self._libssh.ssh_free(session)

    def ssh_channel_new(self, session):
        return self._libssh.ssh_channel_new(session)

    def ssh_channel_open_session(self, channel):
        return self._libssh.ssh_channel_open_session(channel)

    def ssh_channel_request_exec(self, channel, command):
        return self._libssh.ssh_channel_request_exec(channel, command)

    def ssh_channel_read(self, channel, chunk_size):
        buffer = ctypes.create_string_buffer(chunk_size)
        bytes_read = self._libssh.ssh_channel_read(channel, ctypes.byref(buffer), len(buffer), 0)
        if bytes_read > 0:
            return buffer.value
        else:
            return None

    def ssh_channel_read_nonblocking(self, channel, chunk_size):
        buffer = ctypes.create_string_buffer(chunk_size)
        bytes_read = self._libssh.ssh_channel_read_nonblocking(channel, ctypes.byref(buffer), len(buffer), 0)
        if bytes_read > 0:
            return buffer.value
        else:
            return None

    def ssh_channel_write(self, channel, data):
        return self._libssh.ssh_channel_write(channel, data, len(data))

    def ssh_channel_is_eof(self, channel):
        return self._libssh.ssh_channel_is_eof(channel)

    def ssh_channel_send_eof(self, channel):
        self._libssh.ssh_channel_send_eof(channel)

    def ssh_channel_is_open(self, channel):
        return self._libssh.ssh_channel_is_open(channel)

    def ssh_channel_get_exit_status(self, channel):
        return self._libssh.ssh_channel_get_exit_status(channel)

    def ssh_channel_close(self, channel):
        self._libssh.ssh_channel_close(channel)

    def ssh_channel_free(self, channel):
        self._libssh.ssh_channel_free(channel)

    def ssh_channel_request_pty(self, channel):
        return self._libssh.ssh_channel_request_pty(channel)

    def ssh_channel_request_shell(self, channel):
        return self._libssh.ssh_channel_request_shell(channel)

    def get_error(self, session):
        return self._libssh.ssh_get_error(session)

    def set_hostname(self, session, hostname=b'localhost'):
        self._libssh.ssh_options_set(session, SSH_OPTIONS_HOST, hostname)

    def set_port(self, session, port=b'22'):
        self._libssh.ssh_options_set(session, SSH_OPTIONS_PORT_STR, port)

    def set_private_keyfile(self, session, keyfile=b''):
        self._libssh.ssh_options_set(session, SSH_OPTIONS_IDENTITY, keyfile)

    def set_username(self, session, username=b''):
        self._libssh.ssh_options_set(session, SSH_OPTIONS_USER, username)

