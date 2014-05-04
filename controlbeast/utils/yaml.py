# -*- coding: utf-8 -*-
"""
    controlbeast.utils.yaml
    ~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
import os
import yaml
from controlbeast.conf import CbConf
from controlbeast.utils.dynamic import CbDynamicIterable
from controlbeast.utils.file import CbFile


class CbYaml(CbDynamicIterable, CbFile):
    """
    Wrapper class providing access to YAML data sources.

    This wrapper allows using Python format strings within YAML source
    files, referring to any name defined in :py:mod:`~controlbeast.conf.default`.
    """

    #: File name of the YAML file used as data source
    _filename = None

    def __init__(self, filename=''):
        """
        CbYaml constructor
        """
        if self._check_file_exists(filename) and self._check_access(filename, os.R_OK):
            self._filename = filename
        if self._filename:
            conf = CbConf.get_instance()
            with open(self._filename, 'r') as fp:
                content = fp.read()
                content = content.format(**conf)
                yaml_dict = yaml.safe_load(content)
        else:
            yaml_dict = None
        super(CbYaml, self).__init__(dict=yaml_dict)

    @property
    def filename(self):
        """
        File name of the YAML file to read from.
        Expected to be a string representing a valid and accessible YAML file.
        """
        return self._filename
