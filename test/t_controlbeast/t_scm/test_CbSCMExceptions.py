# -*- coding: utf-8 -*-
"""
    test.t_controlbeast.t_scm.test_Exceptions
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
from unittest import TestCase
from controlbeast.scm.base import CbSCMError, CbSCMInitError, CbSCMCommitError, CbSCMBinaryError, CbSCMRepoError


class TestCbSCMExceptions(TestCase):
    """
    Class providing unit tests for SCM exceptions.

    **Covered test cases:**

    ==============  ========================================================================================
    Test Case       Description
    ==============  ========================================================================================
    01              Try raising a :py:exc:`~controlbeast.scm.CbSCMError` exception.
    02              Try raising a :py:exc:`~controlbeast.scm.CbSCMBinaryError` exception with binary indication.
    03              Try raising a :py:exc:`~controlbeast.scm.CbSCMBinaryError` exception without binary indication.
    04              Try raising a :py:exc:`~controlbeast.scm.CbSCMInitError` exception with text indication.
    05              Try raising a :py:exc:`~controlbeast.scm.CbSCMInitError` exception without text indication.
    06              Try raising a :py:exc:`~controlbeast.scm.CbSCMCommitError` exception with text indication.
    07              Try raising a :py:exc:`~controlbeast.scm.CbSCMCommitError` exception without text indication.
    08              Try raising a :py:exc:`~controlbeast.scm.CbSCMRepoError` exception with text indication.
    09              Try raising a :py:exc:`~controlbeast.scm.CbSCMRepoError` exception without text indication.
    ==============  ========================================================================================
    """

    def test_01(self):
        """
        Test Case 01:
        Try raising a :py:exc:`~controlbeast.scm.CbSCMError` exception.

        Test is passed if expected exception is raised.
        """
        with self.assertRaises(CbSCMError):
            raise CbSCMError

    def test_02(self):
        """
        Test Case 02:
        Try raising a :py:exc:`~controlbeast.scm.CbSCMBinaryError` exception with binary indication.

        Test is passed if exception string matches expectation.
        """
        try:
            raise CbSCMBinaryError(scm_name='git')
        except CbSCMBinaryError as err:
            self.assertEqual(str(err), "git is not available on your computer.")

    def test_03(self):
        """
        Try raising a :py:exc:`~controlbeast.scm.CbSCMBinaryError` exception without binary indication.

        Test is passed if exception string matches expectation.
        """
        try:
            raise CbSCMBinaryError()
        except CbSCMBinaryError as err:
            self.assertEqual(str(err), "Expected SCM is not available on your computer.")

    def test_04(self):
        """
        Test Case 04:
        Try raising a :py:exc:`~controlbeast.scm.CbSCMInitError` exception with text indication.

        Test is passed if exception string matches expectation.
        """
        try:
            raise CbSCMInitError(path='test', text="Test message.")
        except CbSCMInitError as err:
            self.assertEqual(str(err), "Initialisation of test failed:\nTest message.")

    def test_05(self):
        """
        Test Case 05:
        Try raising a :py:exc:`~controlbeast.scm.CbSCMInitError` exception without text indication.

        Test is passed if exception string matches expectation.
        """
        try:
            raise CbSCMInitError(path='test')
        except CbSCMInitError as err:
            self.assertEqual(str(err), "Initialisation of test failed for unknown reason.")

    def test_06(self):
        """
        Test Case 06:
        Try raising a :py:exc:`~controlbeast.scm.CbSCMCommitError` exception with text indication.

        Test is passed if exception string matches expectation.
        """
        try:
            raise CbSCMCommitError(path='test', text="Test message.")
        except CbSCMCommitError as err:
            self.assertEqual(str(err), "Commit to test failed:\nTest message.")

    def test_07(self):
        """
        Test Case 07:
        Try raising a :py:exc:`~controlbeast.scm.CbSCMCommitError` exception without text indication.

        Test is passed if exception string matches expectation.
        """
        try:
            raise CbSCMCommitError(path='test')
        except CbSCMCommitError as err:
            self.assertEqual(str(err), "Commit to test failed for unknown reason.")

    def test_08(self):
        """
        Test Case 08:
        Try raising a :py:exc:`~controlbeast.scm.CbSCMRepoError` exception with text indication.

        Test is passed if exception string matches expectation.
        """
        try:
            raise CbSCMRepoError(path='test', text="Test message.")
        except CbSCMRepoError as err:
            self.assertEqual(str(err), "Repository at test is not valid:\nTest message.")

    def test_09(self):
        """
        Test Case 09:
        Try raising a :py:exc:`~controlbeast.scm.CbSCMRepoError` exception without text indication.

        Test is passed if exception string matches expectation.
        """
        try:
            raise CbSCMRepoError(path='test')
        except CbSCMRepoError as err:
            self.assertEqual(str(err), "Repository at test is not valid.")
