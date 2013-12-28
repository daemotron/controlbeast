# -*- coding: utf-8 -*-
"""
    test.t_controlbeast.t_ssh.test_CbSSHApi
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
from unittest import TestCase
from controlbeast.ssh.api import CbSSHLib


class TestCbSSHApi(TestCase):
    """
    Class providing unit tests for SSH API.

    **Covered test cases:**

    ==============  ========================================================================================
    Test Case       Description
    ==============  ========================================================================================
    01              Try instantiating an SSH API object by its *get_instance* class method.
    02              Try instantiating an SSH API object directly.
    03              Compare two :py:class:`~controlbeast.ssh.api.CbSSHLib` instances.
    ==============  ========================================================================================
    """

    def test_01(self):
        """
        Test Case 01:
        Try instantiating an SSH API object by its *get_instance* class method.

        Test is passed if the API instance proves being a :py:class:`~controlbeast.ssh.api.CbSSHLib` instance.
        """
        obj = CbSSHLib.get_instance()
        self.assertIsInstance(obj, CbSSHLib)

    def test_02(self):
        """
        Test Case 02:
        Try instantiating an SSH API object directly.

        Test is passed if a :py:exc:`TypeError` exception is raised.
        """
        with self.assertRaises(TypeError):
            obj = CbSSHLib()

    def test_03(self):
        """
        Test Case 03:
        Compare two :py:class:`~controlbeast.ssh.api.CbSSHLib` instances.

        Test is passed if both instances are identical.
        """
        obj_1 = CbSSHLib.get_instance()
        obj_2 = CbSSHLib.get_instance()
        self.assertEqual(obj_1, obj_2)
