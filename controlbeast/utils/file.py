# -*- coding: utf-8 -*-
"""
    controlbeast.utils.file
    ~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
import os


class CbFile(object):
    """
    Meta class providing methods for classes that have to deal with
    file system objects.
    """

    @staticmethod
    def _check_access(file, mode) -> bool:
        """
        Checks if a file system object can be accessed in a specific mode
        """
        # perform test on effective [g,u]uid on platforms supporting this in order to
        # grant respecting an eventually set SUID bit
        status = False
        if os.access in os.supports_effective_ids:
            # noinspection PyArgumentList
            status = os.access(file, mode, effective_ids=True)
        else:
            # noinspection PyArgumentList
            status = os.access(file, mode, effective_ids=False)
        return status

    @staticmethod
    def _check_file_exists(filename) -> bool:
        """
            Checks if a file does exist and is a regular file
            :param str filename:    name of the file to be tested
            :return:                True if the file exists, False if not
            :rtype:                 bool
            """
        return os.path.exists(os.path.abspath(filename)) and os.path.isfile(os.path.abspath(filename))

    @staticmethod
    def _check_dir_exists(path) -> bool:
        """
        Checks if a path exists and is a directory

        :param str path:    name of the path to be tested
        :return:            True if the path exists, False if not
        :rtype:             bool
        """
        return os.path.exists(os.path.abspath(path)) and os.path.isdir(os.path.abspath(path))
