ControlBeast SSH Interface
==========================

General SSH Interface
---------------------

.. currentmodule:: controlbeast.ssh

.. autofunction:: connect


SSH Session Object
------------------

.. currentmodule:: controlbeast.ssh.session

.. autoclass:: CbSSHSession
   :members:


SSH Shell Object
----------------

.. currentmodule:: controlbeast.ssh.shell

.. autoclass:: CbSSHShell
   :members:


SSH Result Objects
------------------

.. currentmodule:: controlbeast.ssh.result

.. autoclass:: CbSSHLazyResult
   :members:

.. autoclass:: CbSSHResult
   :show-inheritance:
   :members:


SSH Key Generation
------------------

.. currentmodule:: controlbeast.ssh.keygen

.. autoclass:: CbSSHKeygen
   :members:


SSH Agent
---------

.. currentmodule:: controlbeast.ssh.agent

.. autoclass:: CbSSHAgent
   :members:


Exceptions
----------

.. currentmodule:: controlbeast.ssh.exception

.. autoexception:: controlbeast.ssh.exception.CbSSHError

.. autoexception:: controlbeast.ssh.exception.CbSSHLibraryError

.. autoexception:: controlbeast.ssh.exception.CbSSHConnectionError

.. autoexception:: controlbeast.ssh.exception.CbSSHAuthenticationError

.. autoexception:: controlbeast.ssh.exception.CbSSHCommunicationError

.. autoexception:: controlbeast.ssh.exception.CbSSHExecutionError

.. autoexception:: controlbeast.ssh.exception.CbSSHAgentError


SSH Library API
---------------

.. currentmodule:: controlbeast.ssh.api

.. autoclass:: CbSSHLib()
   :members:

   .. method:: ssh_new

      Create a new libssh session object.

      :returns: libssh session object

   .. method:: ssh_connect(session)

      Open an SSH connection.

      :param session: the libssh session object to be used for the connection
      :returns: libssh return code
      :rtype: :class:`int`

   .. method:: ssh_auth_pubkey(session, passphrase)

      Authenticate to an open SSH session using the public key authentication method.

      :param session: the libssh session object holding the open connection
      :param bytes passphrase: passphrase eventually needed to de-cypher the SSH private key
      :returns: libssh return code
      :rtype: :class:`int`

   .. method:: ssh_auth_password(session, password)

      Authenticate to an open SSH session using the password authentication method.

      .. warning::

         There currently seems to be an issue with libssh and password authentication, at least in
         conjunction with FreeBSD 10 (OpenSSH >=6.4).

      :param session: the libssh session object holding the open connection
      :param bytes password: password to be used for password authentication
      :returns: libssh return code
      :rtype: :class:`int`

   .. method:: ssh_disconnect(session)

      Disconnect an open SSH connection.

      :param session: the libssh session object holding the connection to be closed

   .. method:: ssh_free(session)

      Free an allocated libssh session object.

      :param session: the libssh session object to be eradicated

      .. warning::

         After having freed a libssh session object, it cannot be used to re-connect. A new libssh session object
         would then have to be acquired using the :py:meth:`~controlbeast.ssh.api.CbSSHLib.ssh_new` method.

   .. method:: ssh_channel_new(session)

      Create a new libssh channel object

      :param session: libssh session object to open the channel on
      :returns: libssh channel object

   .. method:: ssh_channel_open_session(channel)

      Open communication session on channel object

      :param channel: libssh channel object
      :returns: libssh return code
      :rtype: :class:`int`

   .. method:: ssh_channel_request_exec(channel, command)

      Request remote execution of a command

      :param channel: libssh channel object
      :param bytes command: byte sequence representing the command string requested to be executed remotely
      :returns: libssh return code
      :rtype: :class:`int`

   .. method:: ssh_channel_read(channel, chunk_size)

      Read `chunk_size` bytes from an open SSH communication channel.

      :param channel: libssh channel object
      :param int chunk_size: number of bytes to be read from the SSH channel
      :returns: vector of read bytes or None

   .. method:: ssh_channel_read_nonblocking(channel, chunk_size)

      Read `chunk_size` bytes from an open SSH communication channel in non-blocking mode.

      :param channel: libssh channel object
      :param int chunk_size: number of bytes to be read from the SSH channel
      :returns: vector of read bytes or None

   .. method:: ssh_channel_write(channel, data)

      Write data into SSH communication channel.

      :param channel: libssh channel object
      :param bytes data: vector of bytes to be written into SSH channel

   .. method:: ssh_channel_is_eof(channel)

      Test if SSH communication channel is EoF.

      :param channel: libssh channel object
      :returns: libssh return code
      :rtype: :class:`int`

   .. method:: ssh_channel_send_eof(channel)

      Send EOF on an open SSH communication channel.

      :param channel: libssh channel object

   .. method:: ssh_channel_is_open(channel)

      Test if SSH communication channel is open.

      :param channel: libssh channel object
      :returns: libssh return code
      :rtype: :class:`int`

   .. method:: ssh_channel_get_exit_status(channel)

      Get the exit status from the last command executed on this SSH communication channel

      :param channel: libssh channel object
      :returns: SSH channel return code
      :rtype: :class:`int`

   .. method:: ssh_channel_close(channel)

      Close an open SSH communication channel.

      :param channel: libssh channel object to be eradicated

   .. method:: ssh_channel_free(channel)

      Free an allocated libssh channel object

      :param channel: libssh channel object to be eradicated

   .. method:: ssh_channel_request_pty(channel)

      Set up a PTY within the SSH communication channel

      :param channel: libssh channel object
      :returns: libssh return code
      :rtype: :class:`int`

   .. method:: ssh_channel_request_shell(channel)

      Set up a shell within the SSH communication channel

      .. note::

         This will only work if a PTY has been set up before for the same SSH channel object!

      :param channel: libssh channel object
      :returns: libssh return code
      :rtype: :class:`int`

   .. method:: get_error(session)

      Get the message describing the latest occurred error.

      :param session: the libssh session object on which the error occurred
      :returns: the message describing the latest occurred error
      :rtype: :class:`bytes`

   .. method:: set_hostname(session, hostname=b'localhost')

      Set the hostname for a libssh session object.

      :param session: the libssh session object to apply the hostname change to
      :param bytes hostname: byte sequence representing the hostname or IP address

   .. method:: set_port(session, port=b'22')

      Set the remote port for a libssh session object.

      :param session: the libssh session object to apply the port change to
      :param bytes port: byte sequence representing the remote port

   .. method:: set_private_keyfile(session, keyfile=b'')

      Set the path of a private key file to be used for authentication.

      :param session: the libssh session object to apply the key file change to
      :param bytes keyfile: byte sequence representing the path of a private key file

   .. method:: set_username(session, username=b'')

      Set the remote username for a libssh session object.

      :param session: the libssh session object to apply the username change to
      :param bytes username: byte sequence representing the remote username
