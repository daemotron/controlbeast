# -*- coding: utf-8 -*-
"""
    test.t_controlbeast.t_keystore.test_CbKeyStore
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
import os
import tempfile
from unittest import TestCase
import yaml
from controlbeast.keystore import CbKeyStore, CbKsIOError, CbKsPasswordError


class TestCbKeyStore(TestCase):
    """
    Class providing unit tests for the CbKeyStore class.

    **Covered Test Cases**

    =========  ==========  ==============  ===========  ===============  ================  ============  =========
    Test Case  Backend     Temporary File  File Exists  File accessible  Password correct  Initial Data  Operation
    =========  ==========  ==============  ===========  ===============  ================  ============  =========
    01         CbKsPlain   True            N/A          N/A              N/A               False         create
    02         CbKsPlain   True            N/A          N/A              N/A               False         update
    03         CbKsPlain   True            N/A          N/A              N/A               False         delete
    04         CbKsPlain   True            N/A          N/A              N/A               False         destroy
    05         CbKsPlain   True            N/A          N/A              N/A               True          create
    06         CbKsPlain   False           False        True             N/A               False         create
    07         CbKsPlain   False           False        False            N/A               False         create
    08         CbKsPlain   False           True         True             N/A               False         create
    09         CbKsCrypto  True            False        True             True              True          create
    10         CbKsCrypto  True            False        True             False             True          create
    11         CbKsPlain   False           True         True             N/A               Broken        create
    12         CbKsPlain   True            N/A          N/A              N/A               True          write
    13         CbKsPlain   True            N/A          N/A              N/A               True          delete
    14         CbKsPlain   True            N/A          N/A              N/A               True          sync
    =========  ==========  ==============  ===========  ===============  ================  ============  =========
    """

    def test_01(self):
        """
        Test Case 01:
        Create a key store with plaintext backend using a temporary file.

        Test is passed if the key store instance proves being a :py:class:`~controlbeast.keystore.CbKeyStore` instance.
        """
        obj = CbKeyStore()
        self.assertIsInstance(obj, CbKeyStore)

    def test_02(self):
        """
        Test Case 02:
        Update data on a key store with plaintext backend using a temporary file.

        Test is passed if dictionary constructed via `PyYAML`_ from file content equals
        the key store object content-wise.

        .. _PyYAML: http://pyyaml.org/
        """
        obj = CbKeyStore()
        obj['test'] = 'success'
        # a key store object is not really a dictionary, it only behaves as if it were one
        comp_1 = dict(obj)
        with open(obj.file, 'r') as file_handle:
            comp_2 = yaml.safe_load(file_handle)
        self.assertDictEqual(comp_1, comp_2)

    def test_03(self):
        """
        Test Case 03:
        Delete data from a key store with plaintext backend using a temporary file.

        Test is passed if key store object *after* deletion equals a reference dictionary content-wise.
        """
        obj = CbKeyStore()
        obj['test1'] = 'delete me'
        obj['test2'] = 'keep me'
        del obj['test1']
        comp_1 = dict(obj)
        comp_2 = {'test2': 'keep me'}
        self.assertDictEqual(comp_1, comp_2)

    def test_04(self):
        """
        Test Case 04:
        Destroy a :py:class:`~controlbeast.keystore.CbKeyStore` object after having used it.

        Test is passed if no temporary file is left behind on the file system.
        """
        obj = CbKeyStore()
        obj['test'] = 'destroy me'
        filename = obj.file
        self.assertTrue(os.path.exists(filename))
        obj = None
        self.assertFalse(os.path.exists(filename))

    def test_05(self):
        """
        Test Case 05:
        Initialise a key store with plaintext backend using a temporary file with initial data.

        Test is passed if key store object *after* initialisation equals reference dictionary content-wise.
        """
        comp_1 = {'test1': 'dict'}
        comp_2 = {'test2': 'kwargs'}
        obj = CbKeyStore(dict=comp_1, **comp_2)
        comp_1.update(comp_2)
        comp_2 = dict(obj)
        self.assertDictEqual(comp_1, comp_2)

    def test_06(self):
        """
        Test Case 06:
        Create a key store with plaintext backend on a non-existing file, but at a writeable location.

        Test is passed if dictionary constructed via `PyYAML`_ from file content equals
        the key store object content-wise.

        .. _PyYAML: http://pyyaml.org/
        """
        # find a suitable location where we can construct a file
        with tempfile.NamedTemporaryFile() as tmp:
            filename = tmp.name
        obj = CbKeyStore(file=filename)
        obj['test'] = 'success'
        # a key store object is not really a dictionary, it only behaves as if it were one
        comp_1 = dict(obj)
        with open(obj.file, 'r') as file_handle:
            comp_2 = yaml.safe_load(file_handle)
        self.assertDictEqual(comp_1, comp_2)
        # clean up
        obj = None
        os.unlink(filename)

    def test_07(self):
        """
        Test Case 07:
        Try creating a key store with plaintext backend on a non-existing file at a non-writeable location.

        Test is passed if :py:exc:`~controlbeast.keystore.CbKsIOError` exception gets raised and no instance of
        :py:class:`~controlbeast.keystore.CbKeyStore` is created.
        """
        filename = '/root/ks_test.yaml'
        with self.assertRaises(CbKsIOError):
            __ = CbKeyStore(file=filename)

    def test_08(self):
        """
        Test Case 08:
        Create a key store with plaintext backend on an existing file.

        Test is passed if key store object *after* initialisation equals original data content-wise.
        """
        comp_1 = {'test': 'success'}
        fp, name = tempfile.mkstemp()
        os.write(fp, yaml.safe_dump(comp_1).encode())
        os.close(fp)
        obj = CbKeyStore(file=name)
        self.assertDictEqual(comp_1, dict(obj))
        os.unlink(name)

    def test_09(self):
        """
        Test Case 09:
        Create a key store with crypto backend on a temporary file.

        Test is passed if a second key store object using the same credentials equals the reference data content-wise.
        """
        comp = {'test': 'success'}
        obj_1 = CbKeyStore(passphrase='secret', dict=comp)
        self.assertDictEqual(comp, dict(obj_1))
        obj_2 = CbKeyStore(file=obj_1.file, passphrase='secret')
        self.assertDictEqual(comp, dict(obj_2))
        # destroy objects in the right order, since obj_1 is only temporary
        obj_2 = None
        obj_1 = None

    def test_10(self):
        """
        Test Case 10:
        Create a key store with crypto backend on a temporary file.

        Test is passed if a second key store object using wrong credentials causes a
        :py:exc:`~controlbeast.keystore.CbKsPasswordError` to be raised.
        """
        comp = {'test': 'success'}
        obj_1 = CbKeyStore(passphrase='secret', dict=comp)
        with self.assertRaises(CbKsPasswordError):
            obj_2 = CbKeyStore(file=obj_1.file, passphrase='sacred')
        # Clean up
        del obj_1

    def test_11(self):
        """
        Test Case 11:
        Create a key store with plaintext backend on an existing file with invalid content.

        The test is passed if the key store object is empty and read-only in order to preventing
        some file content being destroyed by mistakenly using it as a key store backend file.
        """
        fp, name = tempfile.mkstemp()
        os.write(fp, b'-\n-e')
        os.close(fp)
        obj = CbKeyStore(file=name)
        self.assertDictEqual(dict(obj), {})
        self.assertTrue(obj.read_only)
        os.unlink(name)

    def test_12(self):
        """
        Test Case 12:
        Try writing to a read-only key store.

        The test is passed if :py:exc:`TypeError` is raised.
        """
        comp = {'test': 'success'}
        obj = CbKeyStore(dict=comp)
        obj.read_only = True
        with self.assertRaises(TypeError):
            obj['foo'] = 'bar'
        del obj

    def test_13(self):
        """
        Test Case 13:
        Try deleting from a read-only key store.

        The test is passed if :py:exc:`TypeError` is raised.
        """
        comp = {'test': 'success'}
        obj = CbKeyStore(dict=comp)
        obj.read_only = True
        with self.assertRaises(TypeError):
            del obj['test']
        del obj

    def test_14(self):
        """
        Test Case 14:
        Try force-syncing a read-only key store.

        The test is passed if :py:exc:`TypeError` is raised.
        """
        comp = {'test': 'success'}
        obj = CbKeyStore(dict=comp)
        obj.read_only = True
        with self.assertRaises(TypeError):
            # noinspection PyProtectedMember
            obj._sync()
        del obj
