# -*- coding: utf-8 -*-
"""
    controlbeast.ssh
    ~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
from controlbeast.ssh.session import CbSSHSession


def connect(hostname='localhost', port='22', username='', password='', passphrase='', private_key_file=''):
    """
    Connect to a remote host via SSH.

    The SSH session object returned by this function behaves lazily, meaning it will only
    establish the connection as soon as it is actually needed.

    :param str hostname: remote ip address or hostname
    :param str port: remote SSH port
    :param str username: remote username to be used for authentication
    :param str password: remote user's password
    :param str passphrase: passphrase for accessing a (local) private key for authentication
    :param str private_key_file: path to the private key file to be used for authentication
    :return: SSH session object
    :rtype: :py:class:`~controlbeast.ssh.session.CbSSHSession`
    """
    return CbSSHSession(hostname, port, username, password, passphrase, private_key_file)