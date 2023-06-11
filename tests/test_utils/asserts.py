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


def assert_rune(test: unittest.TestCase, rune1: Item, rune2: Item):
    test.assertIsNotNone(rune1)
    test.assertEqual(rune2.type, rune1.type)
    test.assertEqual(rune2.chat_link, rune1.chat_link)
    test.assertEqual(rune2.name, rune1.name)
    test.assertEqual(rune2.icon, rune1.icon)
    test.assertEqual(rune2.description, rune1.description)
    test.assertEqual(rune2.rarity, rune1.rarity)
    test.assertEqual(rune2.details.type, rune1.details.type)
    test.assertEqual(rune2.details.infix_upgrade.id,
                     rune1.details.infix_upgrade.id)
    test.assertListEqual(rune2.details.flags,
                         rune1.details.flags)
    test.assertListEqual(rune2.details.infusion_upgrade_flags,
                         rune1.details.infusion_upgrade_flags)


def assert_armor(test: unittest.TestCase, armor1: Item, armor2: Item):
    test.assertIsNotNone(armor1)
    test.assertEqual(armor2.type, armor1.type)
    test.assertEqual(armor2.chat_link, armor1.chat_link)
    test.assertEqual(armor2.name, armor1.name)
    test.assertEqual(armor2.icon, armor1.icon)
    test.assertEqual(armor2.description, armor1.description)
    test.assertEqual(armor2.rarity, armor1.rarity)
    test.assertEqual(armor2.details.type, armor1.details.type)
    test.assertEqual(armor2.details.weight_class,
                     armor1.details.weight_class)
    test.assertEqual(armor2.details.defense, armor1.details.defense)
    test.assertEqual(armor2.details.attribute_adjustment,
                     armor1.details.attribute_adjustment)
    test.assertEqual(armor2.details.infix_upgrade,
                     armor1.details.infix_upgrade)


def assert_infusion(test: unittest.TestCase, infusion1: Item, infusion2: Item):
    test.assertIsNotNone(infusion1)
    test.assertEqual(infusion2.type, infusion1.type)
    test.assertEqual(infusion2.chat_link, infusion1.chat_link)
    test.assertEqual(infusion2.name, infusion1.name)
    test.assertEqual(infusion2.icon, infusion1.icon)
    test.assertEqual(infusion2.description, infusion1.description)
    test.assertEqual(infusion2.rarity, infusion1.rarity)
    test.assertEqual(infusion2.details.type, infusion1.details.type)
    test.assertEqual(infusion2.details.infix_upgrade.id,
                     infusion1.details.infix_upgrade.id)
    test.assertListEqual(infusion2.details.flags,
                         infusion1.details.flags)
    test.assertListEqual(infusion2.details.infusion_upgrade_flags,
                         infusion1.details.infusion_upgrade_flags)
