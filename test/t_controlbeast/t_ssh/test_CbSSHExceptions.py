# -*- coding: utf-8 -*-
"""
    test.t_controlbeast.t_ssh.test_CbSSHExceptions
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
from unittest import TestCase
from controlbeast.ssh.exception import CbSSHError, CbSSHLibraryError, CbSSHConnectionError, CbSSHAuthenticationError, CbSSHCommunicationError, CbSSHExecutionError


class TestCbSSHExceptions(TestCase):
    """
    Class providing unit tests for SSH exceptions.

    **Covered test cases:**

    ==============  ========================================================================================
    Test Case       Description
    ==============  ========================================================================================
    01              Try raising a :py:exc:`~controlbeast.ssh.exception.CbSSHError` exception.
    02              Try raising a :py:exc:`~controlbeast.ssh.exception.CbSSHLibraryError` exception with library indication.
    03              Try raising a :py:exc:`~controlbeast.ssh.exception.CbSSHLibraryError` exception without library indication.
    04              Try raising a :py:exc:`~controlbeast.ssh.exception.CbSSHConnectionError` exception.
    05              Try raising a :py:exc:`~controlbeast.ssh.exception.CbSSHAuthenticationError` exception.
    06              Try raising a :py:exc:`~controlbeast.ssh.exception.CbSSHCommunicationError` exception.
    07              Try raising a :py:exc:`~controlbeast.ssh.exception.CbSSHExecutionError` exception.
    ==============  ========================================================================================
    """

    def test_01(self):
        """
        Test Case 01:
        Try raising a :py:exc:`~controlbeast.ssh.exception.CbSSHError` exception.

        Test is passed if expected exception is raised.
        """
        with self.assertRaises(CbSSHError):
            raise CbSSHError

    def test_02(self):
        """
        Test Case 02:
        Try raising a :py:exc:`~controlbeast.ssh.exception.CbSSHLibraryError` exception with library indication.

        Test is passed if exception string matches expectation.
        """
        try:
            raise CbSSHLibraryError(library='test')
        except CbSSHLibraryError as err:
            self.assertEqual(str(err), "test is not available or incompatible on your computer.")

    def test_03(self):
        """
        Test Case 03:
        Try raising a :py:exc:`~controlbeast.ssh.exception.CbSSHLibraryError` exception without library indication.

        Test is passed if exception string matches expectation.
        """
        try:
            raise CbSSHLibraryError()
        except CbSSHLibraryError as err:
            self.assertEqual(str(err), "libssh is not available or incompatible on your computer.")

    def test_04(self):
        """
        Test Case 04:
        Try raising a :py:exc:`~controlbeast.ssh.exception.CbSSHConnectionError` exception.

        Test is passed if exception string matches expectation.
        """
        try:
            raise CbSSHConnectionError(hostname='test', port='22', return_code=1, message='test message')
        except CbSSHConnectionError as err:
            self.assertEqual(str(err), "Connection to test:22 failed: Error 1: test message")

    def test_05(self):
        """
        Test Case 05:
        Try raising a :py:exc:`~controlbeast.ssh.exception.CbSSHAuthenticationError` exception.

        Test is passed if exception string matches expectation.
        """
        try:
            raise CbSSHAuthenticationError(hostname='test', username='john doe')
        except CbSSHAuthenticationError as err:
            self.assertEqual(str(err), "Authentication to test as john doe failed.")

    def test_06(self):
        """
        Test Case 06:
        Try raising a :py:exc:`~controlbeast.ssh.exception.CbSSHCommunicationError` exception.

        Test is passed if exception string matches expectation.
        """
        try:
            raise CbSSHCommunicationError(hostname='test', return_code=1)
        except CbSSHCommunicationError as err:
            self.assertEqual(str(err), "Communication to test failed. Error code: 1")

    def test_07(self):
        """
        Test Case 07:
        Try raising a :py:exc:`~controlbeast.ssh.exception.CbSSHExecutionError` exception.

        Test is passed if exception string matches expectation.
        """
        try:
            raise CbSSHExecutionError(hostname='test', return_code=1, message='test message', command='test command')
        except CbSSHExecutionError as err:
            self.assertEqual(
                str(err), "Remote execution of command on test failed: Error 1: test message\nCommand: test command"
            )
