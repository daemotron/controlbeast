# -*- coding: utf-8 -*-
"""
    test.t_controlbeast.t_ssh.test_CbSSHResult
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
from unittest import TestCase
from controlbeast.ssh.result import CbSSHLazyResult


class TestCbSSHResult(TestCase):
    """
    Class providing unit tests for SSH Result classes.

    **Covered test cases:**

    ==============  ========================================================================================
    Test Case       Description
    ==============  ========================================================================================
    01              Try instantiating a CbSSHLazyResult object.
    ==============  ========================================================================================

    .. note::

       Testing of the :py:class:`~controlbeast.ssh.result.CbSSHResult` class (non-lazy variant) is not
       possible without having an active SSH connection. This would however require a much more complex
       test environment. Therefore, all other SSH functionality has been tested manually.
    """

    def test_01(self):
        """
        Test Case 01:
        Try instantiating a CbSSHLazyResult object.

        Test is passed if the object proves being a :py:class:`~controlbeast.ssh.result.CbSSHLazyResult` instance.
        """
        obj = CbSSHLazyResult('test', 'test', 'test')
        self.assertIsInstance(obj, CbSSHLazyResult)
