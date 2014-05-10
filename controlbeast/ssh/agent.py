# -*- coding: utf-8 -*-
"""
    controlbeast.ssh.api
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
import os
import re
import subprocess
from controlbeast.ssh.exception import CbSSHAgentError
from controlbeast.utils.binary import CbBinary


class CbSSHAgent(CbBinary):
    """
    Class acting as wrapper to the SSH agent using the ``ssh-add`` command line utility.
    """

    #: Socket of the SSH agent
    _socket = None

    #: SSH Askpass Tool
    _askpass = None

    def __init__(self):
        self._arguments = []
        self._socket = os.getenv('SSH_AUTH_SOCK')
        self._askpass = os.getenv('SSH_ASKPASS')
        super(CbSSHAgent, self).__init__(binary_name='ssh-add')

    def add(self, filename=''):
        """
        Add an identity to the ssh agent.

        :param str filename: file name of the identity file to be added
        """
        self._operate(filename=filename, action='add')

    def delete(self, filename=''):
        """
        Delete an identity from the ssh agent.

        :param str filename: file name of the identity file to be removed
        """
        self._operate(filename=filename, action='delete')

    @property
    def keys(self):
        """
        List of keys currently represented by the agent
        """
        self._arguments = ['-l']
        self._execute()
        keys = []
        pattern = re.compile(
            r'^(?P<keylength>\d+)\s+(?P<fingerprint>[0-9a-fA-F:]+)\s+(?P<filename>.+?)\s\((?P<keytype>\w+?)\)$'
        )
        for line in self.stdout.splitlines():
            result = pattern.search(line)
            if 'filename' in result.groupdict().keys():
                keys.append(result.groupdict()['filename'])
        return keys

    def _operate(self, filename='', action='add'):
        if self._socket:
            if action == 'delete':
                self._arguments = ['-d', os.path.abspath(filename)]
            else:
                self._arguments = [os.path.abspath(filename)]
            if self._askpass:
                self._stdin_dev = subprocess.DEVNULL
            self._execute()
            self._stdin_dev = subprocess.PIPE
            if self.return_code != os.EX_OK:
                raise CbSSHAgentError(message=self.stderr)
        else:
            raise CbSSHAgentError
