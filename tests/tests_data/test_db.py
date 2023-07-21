#!/usr/bin/env python

import os
import shutil
import unittest
from unittest.mock import Mock

from config import ConfigProvider
from data import Db
from model import *


curr_dir = os.path.dirname(os.path.abspath(__file__))
test_db_dir = os.path.join(curr_dir, 'tmp')
test_db_file = os.path.join(test_db_dir, 'data.fs')


class TestDb(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()

        self.test_db_dir = test_db_dir
        self.test_db_file = test_db_file
        self.mock_object = ConfigProvider
        self.mock_object.get_data_dir = Mock(return_value=test_db_dir)
        self.mock_object.get_data_file = Mock(return_value=test_db_file)

    def tearDown(self) -> None:
        super().tearDown()
        del self.data
        shutil.rmtree(self.test_db_dir)

    def test_can_create_db(self) -> None:
        self.data = Db()

    def test_can_create_db_on_user_folder(self) -> None:
        self.test_db_dir = os.path.expanduser(os.path.join('~', 'test-db'))
        self.test_db_file = os.path.expanduser(os.path.join(self.test_db_dir, 'data.fs'))

        mock_object = ConfigProvider
        mock_object.get_data_dir = Mock(return_value=self.test_db_dir)
        mock_object.get_data_file = Mock(return_value=self.test_db_file)

        self.data = Db()
