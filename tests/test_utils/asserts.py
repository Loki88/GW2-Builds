#!/usr/bin/env python

import unittest

from model.api import Item


def assert_sigil(test: unittest.TestCase, sigil1: Item, sigil2: Item):
    test.assertIsNotNone(sigil1)
    test.assertEqual(sigil2.type, sigil1.type)
    test.assertEqual(sigil2.chat_link, sigil1.chat_link)
    test.assertEqual(sigil2.name, sigil1.name)
    test.assertEqual(sigil2.icon, sigil1.icon)
    test.assertEqual(sigil2.description, sigil1.description)
    test.assertEqual(sigil2.rarity, sigil1.rarity)
    test.assertEqual(sigil2.details.type, sigil1.details.type)
    test.assertEqual(sigil2.details.infix_upgrade.id,
                     sigil1.details.infix_upgrade.id)
    test.assertListEqual(sigil2.details.flags,
                         sigil1.details.flags)
    test.assertListEqual(sigil2.details.infusion_upgrade_flags,
                         sigil1.details.infusion_upgrade_flags)


def assert_weapon(test: unittest.TestCase, weapon1: Item, weapon2: Item):
    test.assertIsNotNone(weapon1)
    test.assertEqual(weapon2.type, weapon1.type)
    test.assertEqual(weapon2.chat_link, weapon1.chat_link)
    test.assertEqual(weapon2.name, weapon1.name)
    test.assertEqual(weapon2.icon, weapon1.icon)
    test.assertEqual(weapon2.description, weapon1.description)
    test.assertEqual(weapon2.rarity, weapon1.rarity)
    test.assertEqual(weapon2.details.type, weapon1.details.type)
    test.assertEqual(weapon2.details.damage_type,
                     weapon1.details.damage_type)
    test.assertEqual(weapon2.details.attribute_adjustment,
                     weapon1.details.attribute_adjustment)
    test.assertEqual(weapon2.details.infix_upgrade,
                     weapon1.details.infix_upgrade)
