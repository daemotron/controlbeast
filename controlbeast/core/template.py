# -*- coding: utf-8 -*-
"""
    controlbeast.core.template
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
import os
from controlbeast.conf import get_conf, CbConf
from controlbeast.utils.file import CbFile
from controlbeast.utils.yaml import CbYaml


class CbTemplate(CbFile):
    """
    ControlBeast Template Manager Object.

    The Template Object can be used to deploy ControlBeast templates to
    a specific location on the file system.

    A ControlBeast template consists at least of the template's root directory,
    containing a file named ``__init__.yml``. This file is expected to be in valid
    YAML 1.1 syntax, describing the template's content.

    .. sourcecode:: yaml

       # list of directories to be created by the template
       dirs:
         - dir1
         - dir2
         - dir2/dir3

       # list of files to be deployed by the template
       files:
         - dir1/file1.txt
         - dir2/dir3/file2.txt

    At least one of the ``dirs`` or ``files`` sections must be present; otherwise nothing
    will be deployed. The file templates described in the ``files`` section must be present within
    the template's directory, mirroring the described directory structure. Taking the above-given
    example, the template file ``file1.txt`` must be located within ``dir1`` in the template's root
    directory.

    All template files, including ``__init__.yml`` may use Python format strings with designators
    defined in :py:mod:`controlbeast.conf.default`.

    :param str template:    name of the template to work with
    :param str path:        destination for the template deployment
    """

    #: Name of the template to work with
    _template = None

    #: Path to deploy to
    _path = None

    #: Dictionary constructed form the template's __init__.yml
    _ini = None

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

    def deploy(self):
        """
        Deploy the template onto the file system.
        """
        if not self._ini:
            self._load_template()
        if not self._ini:
            raise RuntimeError('Could not load template. __init__.yml missing or damaged.')
        if 'dirs' in self._ini:
            for dirname in self._ini['dirs']:
                # noinspection PyArgumentList
                os.makedirs(os.path.join(self._path, dirname), exist_ok=True)
        if 'files' in self._ini:
            conf = CbConf.get_instance()
            for filename in self._ini['files']:
                with open(os.path.join(get_conf('TEMPLATE_PATH'), self._template, filename), 'r') as fp:
                    content = fp.read()
                    content = content.format(**conf)
                    with open(os.path.join(self._path, filename), 'w') as wp:
                        wp.write(content)

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
        filename = os.path.join(get_conf('TEMPLATE_PATH'), template, '__init__.yml')
        # noinspection PyTypeChecker
        if self._check_file_exists(filename) and self._check_access(filename, os.R_OK):
            return True
        else:
            return False

    def _load_template(self):
        """
        Load the template information from the template's __init__.yml
        """
        filename = os.path.join(get_conf('TEMPLATE_PATH'), self._template, '__init__.yml')
        self._ini = CbYaml(filename)
