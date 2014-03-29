# -*- coding: utf-8 -*-
"""
    controlbeast.keystore.crypto
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
import os
import shlex
from controlbeast.keystore.exception import CbKsIOError
from controlbeast.utils.binary import CbBinary
from controlbeast.utils.convert import to_bytes, to_str
from controlbeast.utils.compat import set_inheritable


class CbKsCrypto(CbBinary):
    """
    Symmetric de- and encryption backend.

    This crypto handler keeps the ciphertext in a file, while offering to access the plaintext as a property.
    Updating the plaintext automatically entails updating of the ciphertext in the backend file. Example::

       # set up an encrypted file store
       crypto = CbKsCrypto('/my/file', 'secret_password')

       # put some secret content into the file store
       crypto.plaintext = "My very secret content"

       # destroy crypto object
       crypto = None

       # use another crypto object to read from the file store
       crypto_2 = CbKsCrypto('/my/file', 'secret_password')
       print(crypto_2.plaintext)

    :param str file:        path to file already containing or intended to contain the ciphertext
    :param str passphrase:  Passphrase to derive the key from
    """

    #: Cipher suite to be used for crypto operation
    _ciphersuite = 'aes-256-cbc'

    #: File containing the (encrypted) ciphertext
    _file = ''

    #: Passphrase to be used for crypto operation
    _passphrase = b''

    #: Buffer containing the (unencrypted) message
    _plaintext = b''

    #: Flag signalising whether this backend is read-only or not
    _read_only = True

    def __init__(self, file='', passphrase=''):
        if file:
            self._file = os.path.abspath(file)
            self._test_file()
        if passphrase:
            self._passphrase = to_bytes(passphrase)
        self._arguments = []
        self._stdin = None
        super(CbKsCrypto, self).__init__(binary_name='openssl')

    def _decrypt(self):
        """
        Execute decryption from source file
        """
        # Make sure no stdin data is sent when decrypting from a file
        if self._check_access(self._file, os.R_OK):
            self.stdin = None
            self._operate(action='d')
            self._plaintext = self._stdout
        else:
            self._plaintext = b''

    def _encrypt(self):
        """
        Execute encryption into file
        """
        if not self._read_only:
            # Make sure stdin data contains plaintext to be encrypted
            self._stdin = self._plaintext
            self._operate(action='e')
        else:
            self._decrypt()

    def _operate(self, action):
        """
        Execute the actual crypto operation.

        This method actually calls the external OpenSSL binary and executes the
        operation while communicating with the OpenSSL process via pipes.

        Before calling this method, the environment has to be properly set up:

        * for **decryption**, ``self.stdin`` must be set to ``None``
        * for **encryption**, ``self.stdin`` must be set to contain the plaintext to be encrypted

        When run in decryption mode, the generated plaintext resides in ``self.stdout``.

        :param str action: ``d`` means decrypt, ``e`` means encrypt
        """
        fd_pass_r = None
        # build argument list for de- or encryption
        self._arguments = ['enc', '-{}'.format(self._ciphersuite), '-{}'.format(action)]
        if self._ciphersuite != "none":
            # generate file descriptors for pipe needed for transporting the password to the openssl subprocess
            # write the password into our end end close our pipe's end file descriptor
            fd_pass_r, fd_pass_w = os.pipe()
            set_inheritable(fd_pass_r, True)
            os.write(fd_pass_w, self._passphrase)
            os.close(fd_pass_w)
            self._arguments.extend(['-a', '-pass', 'fd:{}'.format(fd_pass_r)])
        if action == 'e':
            self._arguments.extend(['-salt', '-out', shlex.quote(self._file)])
        elif action == 'd':
            self._arguments.extend(['-in', shlex.quote(self._file)])
        # when executing openssl, close_fds must be False; otherwise pipe communication will not work
        self._execute(close_fds=False)
        # close the pipe's remote end file descriptor if it exists
        if self._ciphersuite != "none":
            os.close(fd_pass_r)

    def _test_file(self):
        """
        Check permissions for file selected for backend
        """
        if os.path.isfile(self._file):
            if not self._check_access(self._file, os.R_OK):
                raise CbKsIOError(filename=self._file)
            if self._check_access(self._file, os.W_OK):
                self._read_only = False
        else:
            if not self._check_access(os.path.dirname(self._file), os.W_OK):
                raise CbKsIOError(filename=self._file)
            self._read_only = False

    @property
    def plaintext(self):
        """
        Plaintext either to be encrypted or resulting from ciphertext decryption. Updating the plaintext
        automatically entails updating of the ciphertext in the file backend.
        """
        if not self._plaintext:
            self._decrypt()
        return to_str(self._plaintext)

    @plaintext.setter
    def plaintext(self, value):
        if not self._read_only:
            self._plaintext = to_bytes(value)
            self._encrypt()
        else:
            raise TypeError("This key store backend is read-only.")

    @property
    def read_only(self):
        """
        Boolean indicating whether this backend is read-only or not
        """
        return self._read_only