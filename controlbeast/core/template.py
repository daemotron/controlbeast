# -*- coding: utf-8 -*-
"""
    controlbeast.core.template
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
import os
from controlbeast.conf import get_conf
from controlbeast.utils.file import CbFile


class CbTemplate(CbFile):
    """
    ControlBeast Template Manager Object.

    The Template Object can be used to deploy ControlBeast templates to
    a specific location on the file system.

    :param str template:    name of the template to work with
    :param str path:        destination for the template deployment
    """

    #: Name of the template to work with
    _template = None

    #: Path to deploy to
    _path = None

    def __init__(self, template='', path=None):
        """
        Template Object constructor
        """
        self.template = template
        if not path:
            self.path = os.path.abspath(os.getcwd())
        else:
            self.path = os.path.abspath(path)

    @property
    def path(self):
        """
        Path to deploy the template to.
        Expected to be a string representing a valid path name with write access.
        """
        return self._path

    @path.setter
    def path(self, path):
        if self._check_path(path):
            self._path = path

    @property
    def template(self):
        """
        Name of the ControlBeast Template to work with.
        Expected to be a string representing a valid template name.
        """
        return self._template

    @template.setter
    def template(self, template):
        if self._check_template_name(template):
            self._template = template

    def _check_path(self, path):
        """
        Check whether the given path exists and if yes, if it's writeable.
        :param str path:    Name of the path to be tested
        :return:            True if the path can be used for deployment, False if not
        :rtype:             bool
        """
        result = False
        if self._check_dir_exists(path):
            # ok, path is an existing file system object and a directory. But is it also writeable?
            if self._check_access(os.path.abspath(path), os.W_OK):
                # Perfect.
                result = True
        else:
            # hm, the path doesn't exist. but could we create it? let's find the last existing parent...
            parent = os.path.dirname(os.path.abspath(path))
            while not self._check_dir_exists(parent):
                parent = os.path.dirname(parent)
            if self._check_access(os.path.abspath(parent), os.W_OK):
                # good news, we could create the path
                result = True
        return result

    def _check_template_name(self, template):
        """
        Check whether the given template name is an existing ControlBeast template and can be accessed.

        :param str template:    Name of the template to be verified
        :return:                True if the template is valid, False if not
        :rtype:                 bool
        """
        filename = os.path.join(get_conf('TEMPLATE_PATH'), template), '__init__.yml'
        if self._check_file_exists(filename) and self._check_access(filename, os.R_OK):
            return True
        else:
            return False