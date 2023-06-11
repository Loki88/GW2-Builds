#!/usr/bin/env python

import os
import shutil
import unittest
from unittest.mock import Mock

from config import ConfigProvider
from data import *
from model import *


curr_dir = os.path.dirname(os.path.abspath(__file__))
test_db_dir = os.path.join(curr_dir, 'tmp')
test_db_file = os.path.join(test_db_dir, 'data.fs')


class TestBuildRepository(unittest.TestCase):

    data: Db = None
    repository: BuildRepository = None

    @classmethod
    def setUpClass(cls):
        unittest.TestCase.setUpClass()

        mock_object = ConfigProvider
        mock_object.get_data_dir = Mock(return_value=test_db_dir)
        mock_object.get_data_file = Mock(return_value=test_db_file)

    def setUp(self) -> None:
        super().setUp()
        self.data = Db()
        self.repository = BuildRepository()

    def tearDown(self) -> None:
        super().tearDown()
        del self.repository
        del self.data
        shutil.rmtree(test_db_dir)

    def test_save_build(self):
        # given
        build = Build(1)

        # when
        self.repository.save_build(build)

    def test_get_build(self):
        # given
        build = Build(1)
        self.repository.save_build(build)

        # when
        db_build = self.repository.get_build()

        # then
        self.assertIsNotNone(db_build)
        self.assertEqual(build.build_number, db_build.build_number)
        self.assertIsNotNone(db_build.date)

    def test_delete_build(self):
        # given
        build = Build(1)
        self.repository.save_build(build)
        db_build = self.repository.get_build()
        self.assertIsNotNone(db_build)

        # when
        self.repository.delete_build()
        db_build = self.repository.get_build()

        # then
        self.assertIsNone(db_build)
