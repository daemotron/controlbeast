# -*- coding: utf-8 -*-
"""
    test.t_scripts.test_cb
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
import imp
import os
from unittest import TestCase


class TestScript(TestCase):
    """
    Unit tests for ``scripts/cb.py``
    """

    def test_01_import(self):
        """
        Test 01: importing the cb script should be prohibited
        """
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'cb.py'))
        with self.assertRaises(RuntimeError):
            __ = imp.load_source('cb', path)
