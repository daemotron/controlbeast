# -*- coding: utf-8 -*-
"""
    test.t_controlbeast.test_CB
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""


from unittest import TestCase
from controlbeast import get_version


class TestCbBase(TestCase):
    """
    Class providing unit tests for the ControlBeast module

    **Covered test cases:**

    ==============  ========================================================================================
    Test Case       Description
    ==============  ========================================================================================
    01              Get the ControlBeast version information.
    ==============  ========================================================================================
    """

    def test_01(self):
        """
        Test Case 01:
        Get the ControlBeast version information.

        Test is passed if returned version information is a string.
        """
        self.assertIsInstance(get_version(), str)
