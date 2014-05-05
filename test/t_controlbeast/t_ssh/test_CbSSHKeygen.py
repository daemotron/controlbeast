# -*- coding: utf-8 -*-
"""
    test.t_controlbeast.t_ssh.test_CbSSHKeygen
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
import tempfile
import os
from unittest import TestCase, skipUnless, skipIf
import sys
from controlbeast.ssh import CbSSHKeygen


#: local CbSSHKeygen instance for skip conditions
_ssh = CbSSHKeygen()


class TestCbSSHKeygen(TestCase):
    """
    Class providing unit tests for SSH Result classes.

    **Covered test cases:**

    ==============  ========================================================================================
    Test Case       Description
    ==============  ========================================================================================
    01              Try instantiating a CbSSHKeygen object.
    02              Try detecting the OpenSSH version.
    03              Query list of allowed algorithms.
    04              Query range of allowed key lengths for RSA.
    05              Query range of allowed key lengths for DSA.
    06              Query range of allowed key lengths for ECDSA.
    07              Query range of allowed key lengths for ED25519.
    08              Try setting a valid key length for the RSA algorithm.
    09              Try setting an invalid key length for the RSA algorithm.
    10              Switch algorithm to DSA and verify keylength is set appropriately.
    11              Switch algorithm to RSA and verify keylength is set appropriately.
    12              Switch algorithm to ECDSA and verify keylength is set appropriately.
    13              Switch algorithm to ED25519 and verify keylength is set appropriately.
    14              Try switching to an invalid algorithm.
    15              Try creating a public/private key pair using the RSA algorithm.
    16              Try creating a public/private key pair using the DSA algorithm.
    17              Try creating a public/private key pair using the ECDSA algorithm.
    18              Try creating a public/private key pair using the ED25519 algorithm.
    ==============  ========================================================================================
    """

    def test_01(self):
        """
        Test Case 01:
        Try instantiating a CbSSHKeygen object.

        Test is passed if the object proves being a :py:class:`~controlbeast.ssh.keygen.CbSSHKeygen` instance.
        """
        obj = CbSSHKeygen()
        self.assertIsInstance(obj, CbSSHKeygen)

    def test_02(self):
        """
        Test Case 02:
        Try detecting the OpenSSH version.

        Test is passed if the detected version is a tuple of two integers greater than (0, 0).
        """
        obj = CbSSHKeygen()
        self.assertIsInstance(obj.ssh_version, tuple)
        self.assertIsInstance(obj.ssh_version[0], int)
        self.assertIsInstance(obj.ssh_version[1], int)
        self.assertGreater(obj.ssh_version, (0, 0))

    def test_03(self):
        """
        Test Case 03:
        Query list of allowed algorithms.

        Test is passed if list of algorithms corresponds to detected OpenSSH version.
        """
        obj = CbSSHKeygen()
        if obj.ssh_version < (5, 7):
            self.assertListEqual(obj.algorithms, ['rsa', 'dsa'])
        if (5, 7) <= obj.ssh_version < (6, 5):
            self.assertListEqual(obj.algorithms, ['rsa', 'dsa', 'ecdsa'])
        if obj.ssh_version >= (6, 5):
            self.assertListEqual(obj.algorithms, ['rsa', 'dsa', 'ecdsa', 'ed25519'])

    def test_04(self):
        """
        Test Case 04:
        Query range of allowed key lengths for RSA.

        Test is passed if allowed range corresponds to expected range.
        """
        obj = CbSSHKeygen()
        obj.algorithm = 'rsa'
        self.assertListEqual(obj.key_range, [2048, 4096, 8192, 16384])

    def test_05(self):
        """
        Test Case 05:
        Query range of allowed key lengths for DSA.

        Test is passed if allowed range corresponds to expected range.
        """
        obj = CbSSHKeygen()
        obj.algorithm = 'dsa'
        self.assertListEqual(obj.key_range, [1024])

    @skipUnless(_ssh.ssh_version >= (5, 7), 'ECDSA not available in OpenSSH < 5.7')
    @skipIf(sys.platform == 'darwin', 'ECDSA broken on OS X (Darwin)')
    def test_06(self):
        """
        Test Case 06:
        Query range of allowed key lengths for ECDSA.

        Test is passed if allowed range corresponds to expected range.
        """
        obj = CbSSHKeygen()
        obj.algorithm = 'ecdsa'
        self.assertListEqual(obj.key_range, [256, 384, 512])

    @skipUnless(_ssh.ssh_version >= (6, 5), 'ED25519 not available in OpenSSH < 6.5')
    def test_07(self):
        """
        Test Case 07:
        Query range of allowed key lengths for ED25519.

        Test is passed if allowed range corresponds to expected range.
        """
        obj = CbSSHKeygen()
        obj.algorithm = 'ed25519'
        self.assertListEqual(obj.key_range, [256])

    def test_08(self):
        """
        Test Case 08:
        Try setting a valid key length for the RSA algorithm.

        Test is passed if keylength property corresponds to set key length.
        """
        obj = CbSSHKeygen()
        obj.algorithm = 'rsa'
        obj.keylength = 4096
        self.assertEqual(obj.keylength, 4096)

    def test_09(self):
        """
        Test Case 09:
        Try setting an invalid key length for the RSA algorithm.

        Test is passed if keylength property is not changed.
        """
        obj = CbSSHKeygen()
        key_length = obj.keylength
        obj.keylength = 123
        self.assertEqual(key_length, obj.keylength)

    def test_10(self):
        """
        Test Case 10:
        Switch algorithm to DSA and verify keylength is set appropriately.

        Test is passed if keylength property changes to DSA default.
        """
        obj = CbSSHKeygen()
        obj.algorithm = 'dsa'
        self.assertEqual(obj.keylength, 1024)

    def test_11(self):
        """
        Test Case 11:
        Switch algorithm to RSA and verify keylength is set appropriately.

        Test is passed if keylength property changes to RSA default.
        """
        obj = CbSSHKeygen()
        # Switching forth and back is necessary to trigger change of keylength attribute
        obj.algorithm = 'dsa'
        obj.algorithm = 'rsa'
        self.assertEqual(obj.keylength, 2048)

    @skipUnless(_ssh.ssh_version >= (5, 7), 'ECDSA not available in OpenSSH < 5.7')
    @skipIf(sys.platform == 'darwin', 'ECDSA broken on OS X (Darwin)')
    def test_12(self):
        """
        Test Case 12:
        Switch algorithm to ECDSA and verify keylength is set appropriately.

        Test is passed if keylength property changes to ECDSA default.
        """
        obj = CbSSHKeygen()
        obj.algorithm = 'ecdsa'
        self.assertEqual(obj.keylength, 512)

    @skipUnless(_ssh.ssh_version >= (6, 5), 'ED25519 not available in OpenSSH < 6.5')
    def test_13(self):
        """
        Test Case 13:
        Switch algorithm to ED25519 and verify keylength is set appropriately.

        Test is passed if keylength property changes to ED25519 default.
        """
        obj = CbSSHKeygen()
        obj.algorithm = 'ed25519'
        self.assertEqual(obj.keylength, 256)

    def test_14(self):
        """
        Test Case 14:
        Try switching to an invalid algorithm.

        Test is passed if algorithm property is not changed.
        """
        obj = CbSSHKeygen()
        algorithm = obj.algorithm
        obj.algorithm = 'bad_crypto'
        self.assertEqual(obj.algorithm, algorithm)

    def test_15(self):
        """
        Test Case 15:
        Try creating a public/private key pair using the RSA algorithm.

        Test is passed if two files, ``filename`` and ``filename.pub`` are created during the test and the
        return value of ssh-keygen is zero.
        """
        # find a suitable location where we can construct a file
        with tempfile.NamedTemporaryFile() as tmp:
            filename = tmp.name
        obj = CbSSHKeygen()
        obj.algorithm = 'rsa'
        # use minimum key length for testing purposes
        obj.keylength = 2048
        # make use of the passphrase argument to allow this test to run non-interactively on headless systems
        obj.keygen(filename=filename, passphrase='secret')
        self.assertTrue(os.path.isfile(filename) and os.path.isfile('.'.join((filename, 'pub'))))
        self.assertEqual(obj.return_code, os.EX_OK)
        os.unlink(filename)
        os.unlink('.'.join((filename, 'pub')))

    def test_16(self):
        """
        Test Case 16:
        Try creating a public/private key pair using the DSA algorithm.

        Test is passed if two files, ``filename`` and ``filename.pub`` are created during the test and the
        return value of ssh-keygen is zero.
        """
        # find a suitable location where we can construct a file
        with tempfile.NamedTemporaryFile() as tmp:
            filename = tmp.name
        obj = CbSSHKeygen()
        obj.algorithm = 'dsa'
        # use minimum key length for testing purposes
        obj.keylength = 1024
        # make use of the passphrase argument to allow this test to run non-interactively on headless systems
        obj.keygen(filename=filename, passphrase='secret')
        self.assertTrue(os.path.isfile(filename) and os.path.isfile('.'.join((filename, 'pub'))))
        self.assertEqual(obj.return_code, os.EX_OK)
        os.unlink(filename)
        os.unlink('.'.join((filename, 'pub')))

    @skipUnless(_ssh.ssh_version >= (5, 7), 'ECDSA not available in OpenSSH < 5.7')
    @skipIf(sys.platform == 'darwin', 'ECDSA broken on OS X (Darwin)')
    def test_17(self):
        """
        Test Case 17:
        Try creating a public/private key pair using the ECDSA algorithm.

        Test is passed if two files, ``filename`` and ``filename.pub`` are created during the test and the
        return value of ssh-keygen is zero.
        """
        # find a suitable location where we can construct a file
        with tempfile.NamedTemporaryFile() as tmp:
            filename = tmp.name
        obj = CbSSHKeygen()
        obj.algorithm = 'ecdsa'
        # use minimum key length for testing purposes
        obj.keylength = 256
        # make use of the passphrase argument to allow this test to run non-interactively on headless systems
        obj.keygen(filename=filename, passphrase='secret')
        self.assertTrue(os.path.isfile(filename) and os.path.isfile('.'.join((filename, 'pub'))))
        self.assertEqual(obj.return_code, os.EX_OK)
        os.unlink(filename)
        os.unlink('.'.join((filename, 'pub')))

    @skipUnless(_ssh.ssh_version >= (6, 5), 'ED25519 not available in OpenSSH < 6.5')
    def test_18(self):
        """
        Test Case 18:
        Try creating a public/private key pair using the ED25519 algorithm.

        Test is passed if two files, ``filename`` and ``filename.pub`` are created during the test and the
        return value of ssh-keygen is zero.
        """
        # find a suitable location where we can construct a file
        with tempfile.NamedTemporaryFile() as tmp:
            filename = tmp.name
        obj = CbSSHKeygen()
        obj.algorithm = 'ed25519'
        # use minimum key length for testing purposes
        obj.keylength = 256
        # make use of the passphrase argument to allow this test to run non-interactively on headless systems
        obj.keygen(filename=filename, passphrase='secret')
        self.assertTrue(os.path.isfile(filename) and os.path.isfile('.'.join((filename, 'pub'))))
        self.assertEqual(obj.return_code, os.EX_OK)
        os.unlink(filename)
        os.unlink('.'.join((filename, 'pub')))
