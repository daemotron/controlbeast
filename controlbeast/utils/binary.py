# -*- coding: utf-8 -*-
"""
    controlbeast.utils.binary
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
import os
import subprocess
from controlbeast.utils.convert import to_bytes, to_str
from controlbeast.utils.file import CbFile


class CbBinary(CbFile):
    """
    Auxiliary class to ease implementing classes dealing with execution of external binaries.
    """

    #: Name of the binary to be executed. Needs to be overridden by child class.
    _binary_name = None

    #: Absolute path to the binary. Will be detected during object initialisation.
    _binary_path = None

    #: Input to be sent via stdin. Must be either None or a byte sequence.
    _stdin = None

    #: Output received via stdout
    _stdout = b''

    #: Output received via stderr
    _stderr = b''

    #: Return code of the binary executed
    _return_code = 0

    #: Timeout to be respected
    _timeout = None

    #: Arguments to be passed to the binary
    _arguments = []

    def __init__(self, binary_name=''):
        if binary_name:
            self._binary_name = binary_name
        self._detect_binary()

    def _detect_binary(self):
        """
        Look for the binary and store its path in _binary_path
        """
        # only act if _scm_binary_name has been defined
        if self._binary_name:
            for path in os.get_exec_path():
                binary = os.path.join(path, self._binary_name)
                if self._check_access(binary, os.X_OK):
                    self._binary_path = binary
                    break

    def _execute(self, close_fds=True):
        """
        Create a child process executing the external command.
        """
        arguments = [self._binary_path]
        arguments.extend(self._arguments)
        process = subprocess.Popen(
            arguments, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=close_fds
        )
        try:
            self._stdout, self._stderr = process.communicate(input=self._stdin, timeout=self._timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            self._stdout, self._stderr = process.communicate()
        except subprocess.CalledProcessError:
            pass
        except (OSError, FileNotFoundError):
            pass
        finally:
            self._return_code = process.returncode

    @property
    def stdin(self):
        """
        Data to be sent to the executed binary via stdin.
        Expected to be a string or byte sequence or None.
        """
        return to_str(self._stdin)

    @stdin.setter
    def stdin(self, value):
        if not value:
            self._stdin = None
        else:
            self._stdin = to_bytes(value)

    @property
    def stdout(self):
        """
        Data returned by the executed binary via stdout.
        """
        return to_str(self._stdout)

    @property
    def stderr(self):
        """
        Data returned by the executed binary via stderr.
        """
        return to_str(self._stderr)

    @property
    def return_code(self):
        """
        Return code returned by the executed binary
        """
        return self._return_code
