# -*- coding: utf-8 -*-
"""
    test.t_controlbeast.t_scm.test_CbSCMFunctions
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
import os
import tempfile
from unittest import TestCase
import controlbeast.scm
from controlbeast.scm import get_scm, scm_init, scm_commit, scm_get_root
from controlbeast.scm.git import Git


class TestCbSCMFunctions(TestCase):
    """
    Class providing unit tests for SCM function interface.

    **Covered test cases:**

    ==============  ========================================================================================
    Test Case       Description
    ==============  ========================================================================================
    01              Get an SCM wrapper instance by name.
    02              Get a non-existing SCM wrapper instance by name.
    03              Initialise a git repository by using the SCM function interface.
    04              Commit to an existing git repository by using the SCM function interface.
    05              Find the root of an existing git repository from a subdirectory by using the SCM function interface.
    ==============  ========================================================================================
    """

    def test_01(self):
        """
        Test Case 01:
        Get an SCM wrapper instance by name.

        Test is passed if created instance proves being a :py:class:`~controlbeast.scm.git.Git` instance.
        """
        scm_class = get_scm('Git')
        scm_object = scm_class()
        self.assertIsInstance(scm_object, Git)

    def test_02(self):
        """
        Test Case 02:
        Get a non-existing SCM wrapper instance by name.

        Test is passed if ``None`` is returned.
        """
        self.assertIsNone(get_scm('Gut'))

    def test_03(self):
        """
        Test Case 03:
        Initialise a git repository by using the SCM function interface.

        Test is passed if the repository can be initialised without raising an exception.
        """
        with tempfile.TemporaryDirectory() as td:
            scm_init(path=td)
            self.assertTrue(os.path.isdir(os.path.join(td, '.git')))

    def test_04(self):
        """
        Test Case 04:
        Commit to an existing git repository by using the SCM function interface.

        Test is passed if the commit can be executed without raising an exception.
        """
        with tempfile.TemporaryDirectory() as td:
            scm_init(path=td)
            fp = open(os.path.join(td, 'testfile'), 'w')
            fp.write("Test file content")
            fp.close()
            scm_commit(path=td, message='Test message')
            # noinspection PyProtectedMember
            self.assertIn('testfile', controlbeast.scm._scm_handler.stdout)

    def test_05(self):
        """
        Test Case 05:
        Find the root of an existing git repository from a subdirectory by using the SCM function interface.

        Test is passed if the detected root equals the actual root directory.
        """
        with tempfile.TemporaryDirectory() as td:
            scm_init(path=td)
            start = os.path.join(os.path.abspath(td), 'test', 'test')
            os.makedirs(start)
            self.assertEquals(os.path.realpath(td), scm_get_root(path=start))
