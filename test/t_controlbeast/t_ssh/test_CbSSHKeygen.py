# -*- coding: utf-8 -*-
"""
    test.t_controlbeast.t_ssh.test_CbSSHKeygen
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
import tempfile
import os
from unittest import TestCase
from controlbeast.ssh import CbSSHKeygen


class TestCbSSHKeygen(TestCase):
    """
    Class providing unit tests for SSH Result classes.

    **Covered test cases:**

    ==============  ========================================================================================
    Test Case       Description
    ==============  ========================================================================================
    01              Try instantiating a CbSSHKeygen object.
    02              Try generating a key pair with default settings
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
        Try creating a public/private key pair.

        Test is passed if two files, ``filename`` and ``filename.pub`` are created during the test and the
        return value of ssh-keygen is zero.
        """
        # find a suitable location where we can construct a file
        with tempfile.NamedTemporaryFile() as tmp:
            filename = tmp.name
        obj = CbSSHKeygen()
        obj.keygen(filename=filename, passphrase='secret')
        self.assertTrue(os.path.isfile(filename) and os.path.isfile('.'.join((filename, 'pub'))))
        self.assertEqual(obj.return_code, os.EX_OK)
        os.unlink(filename)
        os.unlink('.'.join((filename, 'pub')))

    # TODO: Write unit tests covering other algorithms, and test CbSSHKeygen object properties