# -*- coding: utf-8 -*-
"""
    test.t_controlbeast.t_scm.test_CbSCMWrapper
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
from unittest import TestCase
from controlbeast.scm import CbSCMWrapper


class TestCbSCMWrapper(TestCase):
    """
    Class providing unit tests for CbSCMWrapper class.

    **Covered test cases:**

    ==============  ========================================================================================
    Test Case       Description
    ==============  ========================================================================================
    01              Try instantiating a CbSCMWrapper object.
    02              Try to call the ``init`` method.
    03              Try to call the ``commit`` method.
    04              Try to call the ``create_branch`` method.
    05              Try to call the ``checkout`` method.
    06              Try to call the ``get_branches`` method.
    07              Try to call the ``get_active_branch`` method.
    08              Try to call the ``get_root`` method.
    ==============  ========================================================================================
    """

    def test_01(self):
        """
        Test Case 01:
        Try instantiating a CbSCMWrapper object.

        Test is passed if the scm wrapper instance proves being a :py:class:`~controlbeast.scm.base.CbSCMWrapper`
        instance.
        """
        obj = CbSCMWrapper('git')
        self.assertIsInstance(obj, CbSCMWrapper)

    def test_02(self):
        """
        Test Case 02:
        Try calling the ``init`` method.

        Test is passed if :py:exc:`NotImplementedError` is raised
        """
        obj = CbSCMWrapper('git')
        with self.assertRaises(NotImplementedError):
            obj.init()

    def test_03(self):
        """
        Test Case 03:
        Try calling the ``commit`` method.

        Test is passed if :py:exc:`NotImplementedError` is raised
        """
        obj = CbSCMWrapper('git')
        with self.assertRaises(NotImplementedError):
            obj.commit()

    def test_04(self):
        """
        Test Case 04:
        Try calling the ``create_branch`` method.

        Test is passed if :py:exc:`NotImplementedError` is raised
        """
        obj = CbSCMWrapper('git')
        with self.assertRaises(NotImplementedError):
            obj.create_branch()

    def test_05(self):
        """
        Test Case 05:
        Try calling the ``checkout`` method.

        Test is passed if :py:exc:`NotImplementedError` is raised
        """
        obj = CbSCMWrapper('git')
        with self.assertRaises(NotImplementedError):
            obj.checkout()

    def test_06(self):
        """
        Test Case 06:
        Try calling the ``get_branches`` method.

        Test is passed if :py:exc:`NotImplementedError` is raised
        """
        obj = CbSCMWrapper('git')
        with self.assertRaises(NotImplementedError):
            obj.get_branches()

    def test_07(self):
        """
        Test Case 07:
        Try calling the ``get_active_branch`` method.

        Test is passed if :py:exc:`NotImplementedError` is raised
        """
        obj = CbSCMWrapper('git')
        with self.assertRaises(NotImplementedError):
            obj.get_active_branch()

    def test_08(self):
        """
        Test Case 07:
        Try calling the ``get_root`` method.

        Test is passed if :py:exc:`NotImplementedError` is raised
        """
        obj = CbSCMWrapper('git')
        with self.assertRaises(NotImplementedError):
            obj.get_root()

