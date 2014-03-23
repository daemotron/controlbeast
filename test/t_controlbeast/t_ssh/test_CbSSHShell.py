# -*- coding: utf-8 -*-
"""
    test.t_controlbeast.t_ssh.test_CbSSHSession
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
from unittest import TestCase
from controlbeast.ssh import CbSSHShell


class TestCbSSHShell(TestCase):
    """
    Class providing unit tests for SSH Result classes.

    **Covered test cases:**

    ==============  ========================================================================================
    Test Case       Description
    ==============  ========================================================================================
    01              Try instantiating a CbSSHShell object.
    ==============  ========================================================================================

    .. note::

       Testing of the other :py:class:`~controlbeast.ssh.shell.CbSSHShell` functionality is not
       possible without creating an active SSH connection. This would however require a much more complex
       test environment. Therefore, all other SSH functionality has been tested manually.
    """

    def test_01(self):
        """
        Test Case 01:
        Try instantiating a CbSSHShell object.

        Test is passed if the object proves being a :py:class:`~controlbeast.ssh.shell.CbSSHShell` instance.
        """
        obj = CbSSHShell()
        self.assertIsInstance(obj, CbSSHShell)
