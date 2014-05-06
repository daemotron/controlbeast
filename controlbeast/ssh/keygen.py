# -*- coding: utf-8 -*-
"""
    controlbeast.ssh.keygen
    ~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""


import os
import shlex
import re
from controlbeast.utils.binary import CbBinary


class CbSSHKeygen(CbBinary):
    """
    Class acting as wrapper for the generation of public keys using the ``ssh-keygen`` command line utility.

    .. warning::

       For security reasons, it is highly recommended to **not** using the passphrase argument for setting
       the private key's encryption passphrase, since this will trigger the passphrase being submitted as command
       line argument. Since the process of generating a key may take several seconds, the password will be
       retrievable in plain text from the user's process list for a considerable amount of time.

       This opening a critical race condition, it is recommended to leaving the passphrase empty. If this is the
       case, ssh-keygen will automatically prompt for an appropriate passphrase using the system's ssh-askpass
       mechanism.

    .. note::

       For compatibility reasons, the standard algorithm used for keys is *RSA*
       for the SSHv2 protocol. The newer *Ed25519* algorithm could replace it
       some day, but probably not before FreeBSD 8.4, 9.x and 10.0 get deprecated
       (OpenSSH 6.5 being the first OpenSSH release offering Ed25519 support will
       most probably enter FreeBSD 10.1).
    """

    #: list of available algorithms
    _algorithms = ['rsa', 'dsa']

    #: mapping of algorithms and key lengths
    _key_map = {
        'rsa': {
            'default': 2048,
            'range': [2 ** x for x in range(11, 15, 1)]
        },
        'dsa': {
            'default': 1024,
            'range': [1024]
        },
        'ecdsa': {
            'default': 512,
            'range': [256, 384, 512]
        },
        'ed25519': {
            'default': 256,
            'range': [256]
        }
    }

    #: algorithm to be used for key generation
    _algorithm = 'rsa'

    #: key length in bytes to be used for key generation
    _keylength = 8192

    #: version of OpenSSH
    _ssh_version = (0, 0)

    def __init__(self):
        self._arguments = []
        super(CbSSHKeygen, self).__init__(binary_name='ssh-keygen')
        self._get_ssh_version()
        if self._ssh_version >= (5, 7) and 'ecdsa' not in self._algorithms:
            self._algorithms.append('ecdsa')
        if self._ssh_version >= (6, 5) and 'ed25519' not in self._algorithms:
            self._algorithms.append('ed25519')

    @property
    def algorithm(self):
        """
        Algorithm to be used for key generation.
        Expected to be a string with the designator understood by *ssh-keygen*
        """
        return self._algorithm

    @algorithm.setter
    def algorithm(self, algorithm):
        if algorithm in self._algorithms:
            self._algorithm = algorithm
        if self._keylength not in self._key_map[self._algorithm]['range']:
            self._keylength = self._key_map[self._algorithm]['default']

    @property
    def algorithms(self):
        """
        List of valid algorithm names.
        This list depends on the available OpenSSH version.
        """
        return self._algorithms

    @property
    def keylength(self):
        """
        Key length in bytes to be used for key generation.
        Expected to be an integer within the valid range for the selected algorithm
        (for RSA e. g. [2¹¹, 2¹² , 2¹³, 2¹⁴], for DSA e. g. [2¹⁰]).
        """
        return self._keylength

    @keylength.setter
    def keylength(self, keylength):
        if keylength in self._key_map[self._algorithm]['range']:
            self._keylength = keylength

    @property
    def key_range(self):
        """
        List of allowed key lengths for the currently chosen algorithm.
        """
        return self._key_map[self._algorithm]['range']

    @property
    def ssh_version(self):
        """
        The version of the detected OpenSSH installation as tuple.
        """
        return self._ssh_version

    def keygen(self, filename='', passphrase=''):
        """
        Generate a public/private key pair and store them in ``filename``, encrypted by ``passphrase``

        :param str filename:    File name to store the private key in. The file name for the public key
                                will be derived from this name by suffixing it with ``.pub``
        :param str passphrase:  The passphrase used for encrypting the private key. Please note this passphrase
                                will only be accepted if it's longer than 4 characters. In case the passphrase
                                being empty or too short, ssh-keygen will ask for a passphrase using the system's
                                ssh-askpass mechanism.
        """
        self._arguments.extend([
            '-q',
            '-t', self._algorithm,
            '-b', str(self._keylength),
            '-O', 'clear',
            '-O', 'permit-pty',
            '-C', shlex.quote('{user}@{host}'.format(user=os.getlogin(), host=os.uname().nodename)),
            '-f', shlex.quote(filename)
        ])
        if passphrase and len(passphrase) > 4:
            self._arguments.extend([
                '-N', shlex.quote(passphrase)
            ])
        self._execute()

    def _get_ssh_version(self):
        """
        Detects the version of the installed OpenSSH client
        """
        ssh_bin = CbBinary(binary_name='ssh')
        ssh_bin._arguments = ['-V']
        ssh_bin._execute()
        pattern = re.compile(r'^.*_(\d+).(\d+)\D+.*$')
        result = pattern.search(ssh_bin.stderr)
        if result:
            self._ssh_version = (int(result.groups()[0]), int(result.groups()[1]))
