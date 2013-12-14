# -*- coding: utf-8 -*-
"""
    controlbeast.keystore.handler
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""


from collections import UserDict
import os
import tempfile
import yaml
from controlbeast.keystore.plain import CbKsPlain
from controlbeast.keystore.crypto import CbKsCrypto


class CbKeyStore(UserDict):
    """
    Key store handler.

    A key store is similar to a normal Python dictionary, except it offers persistence
    by storing its content - optionally encrypted - within a file. Since YAML is used
    for serialisation, a key store is limited to contents which can be represented in
    YAML, such as strings, numbers, and other serializable objects.

    If no ``file`` argument is passed, the key store resorts to using a temporary file
    which will be deleted as soon as the key store object is destroyed.

    If no ``password`` argument is passed, the key store will not encrypt its serialized
    representation within the file.

    .. warning::

       The synchronisation behaviour of this key store class is mostly unidirectional, meaning
       it will take into account the file backend's content only at the moment when the key store
       object is created. If the backend file is changed by any other means (a second key store
       object, an external text editor, ...), the key store will not take into account these
       changes, but overwrite them with the next update on its own data.

       Therefore, it is highly recommended to

       * never create two key store objects operating on the same file
       * use key store objects in an environment preponderantly using read-only access
       * when using key store objects in :py:mod:`multiprocessing` or :py:mod:`threading` environments,
         implement appropriate synchronisation mechanisms (although this will not protect from completely
         external changes to the backend file)

    :param str file:        path to file already containing or intended to contain the key store
    :param str passphrase:  Passphrase to derive the key from, if key store should be encrypted
    """

    #: flag signalizing whether this store is temporary or not
    _tmp = False

    def __init__(self, file='', passphrase='', dict=None, **kwargs):
        """
        Key store constructor
        """
        if file:
            self._file = file
            self._tmp = False
        else:
            fp, self._file = tempfile.mkstemp()
            os.close(fp)
            self._tmp = True
        if passphrase:
            self._backend = CbKsCrypto(file=self._file, passphrase=passphrase)
        else:
            self._backend = CbKsPlain(file=self._file)

        if self._backend.plaintext:
            try:
                data = yaml.safe_load(self._backend.plaintext)
            except yaml.YAMLError:
                data = {}
        else:
            data = {}

        if dict is not None:
            data.update(dict)

        super(CbKeyStore, self).__init__(dict=data, **kwargs)

    def __setitem__(self, key, item):
        """
        Overrides default ``__setitem__`` method. Functionality is identical, except data are synced to the
        backend after executing the data update.
        """
        super(CbKeyStore, self).__setitem__(key, item)
        self._sync()

    def __delitem__(self, key):
        """
        Overrides default ``__delitem__`` method. Functionality is identical, except data are synced to the
        backend after executing the data update.
        """
        super(CbKeyStore, self).__delitem__(key)
        self._sync()

    def __del__(self):
        """
        Clean up when object gets de-referenced
        """
        if self._tmp:
            os.unlink(self._file)

    def _sync(self):
        """
        Synchronize current data into the backend. This method is called every time the data stored in
        this key store are modified.
        """
        self._backend.plaintext = yaml.dump(self.data, default_flow_style=False)