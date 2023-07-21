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

        mock_object = ConfigProvider
        mock_object.get_data_dir = Mock(return_value=test_db_dir)
        mock_object.get_data_file = Mock(return_value=test_db_file)

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

        specializations = SpecializationsRepository().get_specializations()
        self.assertIsNotNone(specializations)
        self.assertTrue(len(specializations) > 0)

        professions = ProfessionsRepository().get_professions()
        self.assertIsNotNone(professions)
        self.assertTrue(len(professions) > 0)

        traits = TraitsRepository().get_trait()
        self.assertIsNotNone(traits)
        self.assertTrue(len(traits) > 0)

        skills = SkillsRepository().get_skills()
        self.assertIsNotNone(skills)
        self.assertTrue(len(skills) > 0)

        stats = StatsRepository().get_stats()
        self.assertIsNotNone(stats)
        self.assertTrue(len(stats) > 0)

        armors = ArmorRepository().get_armor()
        self.assertIsNotNone(armors)
        self.assertTrue(len(armors) > 0)

        weapons = WeaponsRepository().get_weapon()
        self.assertIsNotNone(weapons)
        self.assertTrue(len(weapons) > 0)

        trinkets = TrinketsRepository().get_trinket()
        self.assertIsNotNone(trinkets)
        self.assertTrue(len(trinkets) > 0)

        backs = BackRepository().get_back()
        self.assertIsNotNone(backs)
        self.assertTrue(len(backs) > 0)

        infusions = InfusionRepository().get_infusion()
        self.assertIsNotNone(infusions)
        self.assertTrue(len(infusions) > 0)

        runes = RunesRepository().get_rune()
        self.assertIsNotNone(runes)
        self.assertTrue(len(runes) > 0)

        sigils = SigilsRepository().get_sigil()
        self.assertIsNotNone(sigils)
        self.assertTrue(len(sigils) > 0)

        foods = FoodsRepository().get_food()
        self.assertIsNotNone(foods)
        self.assertTrue(len(foods) > 0)

        utilities = UtilitiesRepository().get_utility()
        self.assertIsNotNone(utilities)
        self.assertTrue(len(utilities) > 0)
