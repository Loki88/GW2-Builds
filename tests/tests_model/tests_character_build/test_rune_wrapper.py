#!/usr/bin/env python

import unittest

from model.api import Item
from model.characted_build import RuneWrapper
from tests.test_utils import build_rune, build_armor


class TestRuneWrapper(unittest.TestCase):

    def _assert_rune(self, db_rune: Item, rune: Item):
        self.assertIsNotNone(db_rune)
        self.assertEqual(rune.type, db_rune.type)
        self.assertEqual(rune.chat_link, db_rune.chat_link)
        self.assertEqual(rune.name, db_rune.name)
        self.assertEqual(rune.icon, db_rune.icon)
        self.assertEqual(rune.description, db_rune.description)
        self.assertEqual(rune.rarity, db_rune.rarity)
        self.assertEqual(rune.details.type, db_rune.details.type)
        self.assertEqual(rune.details.infix_upgrade.id,
                         db_rune.details.infix_upgrade.id)
        self.assertListEqual(rune.details.flags,
                             db_rune.details.flags)
        self.assertListEqual(rune.details.infusion_upgrade_flags,
                             db_rune.details.infusion_upgrade_flags)

    def _assert_armor(self, db_armor: Item, armor: Item):
        self.assertIsNotNone(db_armor)
        self.assertEqual(armor.type, db_armor.type)
        self.assertEqual(armor.chat_link, db_armor.chat_link)
        self.assertEqual(armor.name, db_armor.name)
        self.assertEqual(armor.icon, db_armor.icon)
        self.assertEqual(armor.description, db_armor.description)
        self.assertEqual(armor.rarity, db_armor.rarity)
        self.assertEqual(armor.details.type, db_armor.details.type)
        self.assertEqual(armor.details.weight_class,
                         db_armor.details.weight_class)
        self.assertEqual(armor.details.defense, db_armor.details.defense)
        self.assertEqual(armor.details.attribute_adjustment,
                         db_armor.details.attribute_adjustment)
        self.assertEqual(armor.details.infix_upgrade,
                         db_armor.details.infix_upgrade)

    def test_access_fields(self):
        # given
        item: Item = build_armor()

        # when
        wrapper: RuneWrapper = RuneWrapper(item)

        # then
        self._assert_armor(wrapper, item)

    def test_set_rune(self):
        # given
        item: Item = build_armor()
        wrapper: RuneWrapper = RuneWrapper(item)
        rune: Item = build_rune()

        # when
        wrapper.set_rune(rune)

        # then
        self._assert_armor(wrapper, item)
        self._assert_rune(wrapper.get_rune(), rune)
