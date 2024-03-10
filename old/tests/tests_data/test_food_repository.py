#!/usr/bin/env python

import os
import shutil
import unittest
from unittest.mock import Mock

from config import ConfigProvider
from data import *
from model import *
from model import ItemType, ItemRarity, ConsumableType

curr_dir = os.path.dirname(os.path.abspath(__file__))
test_db_dir = os.path.join(curr_dir, 'tmp')
test_db_file = os.path.join(test_db_dir, 'data.fs')


class TestInfusionsRepository(unittest.TestCase):

    data: Db = None
    repository: FoodsRepository = None

    @classmethod
    def setUpClass(cls):
        unittest.TestCase.setUpClass()

        mockObject = ConfigProvider
        mockObject.get_data_dir = Mock(return_value=test_db_dir)
        mockObject.get_data_file = Mock(return_value=test_db_file)

    def setUp(self) -> None:
        super().setUp()
        self.data = Db()
        self.repository = FoodsRepository()

    def tearDown(self) -> None:
        super().tearDown()
        del self.repository
        del self.data
        shutil.rmtree(test_db_dir)

    def _build_item(self) -> Item:
        data = {
            'id': 1,
            'chat_link': '[abcde1]',
            'name': 'Tet',
            'icon': 'test',
            'description': 'test',
            'type': ItemType.Consumable.name,
            'rarity': ItemRarity.Ascended.name,
            'details': {
                'type': ConsumableType.Food.name,
                'description': 'abc',
                'duration_ms': 30000,
                'recipe_id': 1,
                'apply_count': 1,
                'name': 'Test',
                'icon': 'test'
            }
        }

        return Item(data)

    def _assert_food(self, db_food: Item, food: Item):
        self.assertIsNotNone(db_food)
        self.assertEqual(food.type, db_food.type)
        self.assertEqual(food.chat_link, db_food.chat_link)
        self.assertEqual(food.name, db_food.name)
        self.assertEqual(food.icon, db_food.icon)
        self.assertEqual(food.description, db_food.description)
        self.assertEqual(food.rarity, db_food.rarity)
        self.assertEqual(food.details.type, db_food.details.type)
        self.assertEqual(food.details.type,
                         db_food.details.type)
        self.assertEqual(food.details.description,
                         db_food.details.description)
        self.assertEqual(food.details.duration_ms,
                         db_food.details.duration_ms)
        self.assertEqual(food.details.recipe_id,
                         db_food.details.recipe_id)
        self.assertEqual(food.details.apply_count,
                         db_food.details.apply_count)
        self.assertEqual(food.details.name,
                         db_food.details.name)
        self.assertEqual(food.details.icon,
                         db_food.details.icon)

    def test_save_food(self):
        # given
        food = self._build_item()

        # when
        self.repository.save_food(food)

        # then
        self.assertIsNone(None, "Check that save does not throw")

    def test_get_food(self):
        # given
        food = self._build_item()
        self.repository.save_food(food)

        # when
        foods = self.repository.get_food()

        # then
        self.assertIsNotNone(foods)
        self.assertEqual(len(foods), 1)

        db_food = foods[0]
        self._assert_food(db_food, food)

    def test_get_food_by_id(self):
        # given
        food = self._build_item()
        self.repository.save_food(food)

        # when
        self.assertIsNone(
            self.repository.get_food(id=2))
        db_food = self.repository.get_food(id=1)

        # then
        self._assert_food(db_food, food)

    def test_delete_foods(self):
        # given
        food = self._build_item()
        self.repository.save_food(food)

        # when
        self.repository.delete_food()
        db_food = self.repository.get_food()

        # then
        self.assertListEqual(db_food, [])

    def test_delete_food_by_type(self):
        # given
        food = self._build_item()
        self.repository.save_food(food)

        # when
        self.repository.delete_food(id=1)
        db_food = self.repository.get_food()

        # then
        self.assertListEqual(db_food, [])
