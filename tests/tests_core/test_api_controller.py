#!/usr/bin/env python

import os
import shutil
import unittest
from unittest.mock import Mock

from core import ApiController
from data import *
from config import ConfigProvider

curr_dir = os.path.dirname(os.path.abspath(__file__))
test_db_dir = os.path.join(curr_dir, 'tmp')
test_db_file = os.path.join(test_db_dir, 'data.fs')


class TestApiController(unittest.TestCase):

    data: Db = None

    @classmethod
    def setUpClass(cls):
        unittest.TestCase.setUpClass()

        mockObject = ConfigProvider
        mockObject.get_data_dir = Mock(return_value=test_db_dir)
        mockObject.get_data_file = Mock(return_value=test_db_file)

    def setUp(self) -> None:
        super().setUp()
        self.data = Db()

    def tearDown(self) -> None:
        super().tearDown()
        del self.data
        shutil.rmtree(test_db_dir)

    def test_init(self) -> None:
        # when
        ctrl = ApiController()

        # then
        self.assertIsNotNone(BuildRepository().get_build())
        self.assertIsNotNone(SpecializationsRepository().get_specializations())
        self.assertIsNotNone(ProfessionsRepository.get_professions())
