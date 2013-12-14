# -*- coding: utf-8 -*-
"""
    controlbeast.keystore.plain
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""


from controlbeast.keystore.crypto import CbKsCrypto


class CbKsPlain(CbKsCrypto):
    """
    Backend for the key store handler, storing in plain text.
    """

    #: Cipher suite to be used for crypto operation
    _ciphersuite = 'none'