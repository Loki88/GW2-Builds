#!/usr/bin/env python

import os
import configparser
from utils import Singleton

DEFAULT_SECTION = 'DEFAULT'
PATH = 'Path'
FOLDER = 'Folder'
DATA_FOLDER = 'DataFolder'
PARALLEL_LIMIT = 'ParallelLimit'

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


class ConfigProvider(metaclass=Singleton):

    config: configparser.ConfigParser

    def __init__(self) -> None:
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join(DIR_PATH, 'config.ini'))

    def get_path(self) -> str:
        return self.config[DEFAULT_SECTION][PATH]

    def get_folder(self) -> str:
        return self.config[DEFAULT_SECTION][FOLDER]

    def get_data_folder(self) -> str:
        return self.config[DEFAULT_SECTION][DATA_FOLDER]

    def get_parallel_limit(self) -> str:
        return self.config[DEFAULT_SECTION][PARALLEL_LIMIT]

    def get_home_dir(self) -> str:
        return os.path.join(os.path.expanduser(self.get_path()), self.get_folder())

    def get_data_dir(self) -> str:
        return os.path.join(self.get_home_dir(), 'data')

    def get_data_file(self) -> str:
        return os.path.join(self.get_data_dir(), 'data.fs')
