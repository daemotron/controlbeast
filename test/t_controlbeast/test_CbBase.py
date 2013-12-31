# -*- coding: utf-8 -*-
"""
    test.t_controlbeast.test_CB
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
import os
from unittest import TestCase
from controlbeast import get_conf, get_version


class TestCbBase(TestCase):
    """
    Class providing unit tests for the ControlBeast module

    **Covered test cases:**

    ==============  ========================================================================================
    Test Case       Description
    ==============  ========================================================================================
    01              Get a scalar configuration value with a level one key.
    02              Get a dictionary configuration value with a level three key.
    03              Get a location value from global configuration.
    04              Get the ControlBeast version information.
    ==============  ========================================================================================
    """

    def test_01(self):
        """
        Test Case 01:
        Get a scalar configuration value with a level one key.

        Test is passed if returned configuration value is a string.
        """
        self.assertIsInstance(get_conf('scm'), str)

    def test_02(self):
        """
        Test Case 02:
        Get a dictionary configuration value with a level three key.

        Test is passed of returned configuration value is a dictionary.
        """
        self.assertIsInstance(get_conf('dir.repo.recipes'), dict)

    def test_03(self):
        """
        Test Case 03:
        Get a location value from global configuration.

        Test is passed if returned configuration value corresponds to expected string.
        """
        self.assertEqual(
            os.path.join(get_conf(get_conf('keystore.repo.location')), get_conf('keystore.repo.name')),
            get_conf('keystore.repo')
        )

    def test_04(self):
        """
        Test Case 04:
        Get the ControlBeast version information.

        Test is passed if returned version information is a string.
        """
        self.assertIsInstance(get_version(), str)
