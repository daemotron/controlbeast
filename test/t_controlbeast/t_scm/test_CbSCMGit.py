# -*- coding: utf-8 -*-
"""
    test.t_controlbeast.t_scm.test_CbSCMGit
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
import os
import tempfile
from unittest import TestCase
from controlbeast.scm import CbSCMInitError
from controlbeast.scm.git import Git


class TestCbSCMGit(TestCase):
    """
    Class providing unit tests for Git class.

    **Covered test cases:**

    ==============  ========================================================================================
    Test Case       Description
    ==============  ========================================================================================
    01              Try instantiating a Git object.
    02              Initialise a git repository at an accessible location
    03              Try initialising a git repository at an inaccessible location
    04              Commit a new file into the git repository
    05              Find the root of an existing git repository from a subdirectory
    ==============  ========================================================================================
    """

    def test_01(self):
        """
        Test Case 01:
        Try instantiating a Git object.

        Test is passed if the Git instance proves being a :py:class:`~controlbeast.scm.git.Git` instance.
        """
        obj = Git()
        self.assertIsInstance(obj, Git)

    def test_02(self):
        """
        Test Case 02:
        Initialise a git repository at an accessible location.

        Test is passed if the repository can be initialised without raising an exception.
        """
        with tempfile.TemporaryDirectory() as td:
            obj = Git()
            obj.init(path=td)
            self.assertTrue(os.path.isdir(os.path.join(td, '.git')))

    def test_03(self):
        """
        Test Case 03:
        Try initialising a git repository at an inaccessible location.

        Test is passed if :py:exc:`~controlbeast.scm.base.CbSCMInitError` is raised.
        """
        obj = Git()
        with self.assertRaises(CbSCMInitError):
            obj.init(path='/root')

    def test_04(self):
        """
        Test Case 04:
        Commit a new file into an existing git repository.

        Test is passed if the commit can be executed without raising an exception.
        """
        with tempfile.TemporaryDirectory() as td:
            obj = Git()
            obj.init(path=td)
            fp = open(os.path.join(td, 'testfile'), 'w')
            fp.write("Test file content")
            fp.close()
            obj.commit(path=td, message="Test message")
            self.assertIn('testfile', obj.stdout)

    def test_05(self):
        """
        Test Case 05:
        Find the root of an existing git repository from a subdirectory.

        Test is passed if the detected root equals the actual root directory.
        """
        with tempfile.TemporaryDirectory() as td:
            obj = Git()
            obj.init(path=td)
            start = os.path.join(os.path.abspath(td), 'test', 'test')
            os.makedirs(start)
            self.assertEquals(os.path.realpath(td), obj.get_root(path=start))
