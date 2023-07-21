#!/usr/bin/env python

import unittest

from model.api import Item
from model.characted_build import SigilWrapper
from model.enums import WeaponType
from tests.test_utils import build_sigil, build_weapon, assert_weapon, assert_sigil


class TestInfusionWrapper(unittest.TestCase):

    def test_access_fields(self):
        # given
        item: Item = build_weapon()

        # when
        wrapper: SigilWrapper = SigilWrapper(item)

        # then
        assert_weapon(self, wrapper, item)
        self.assertEqual(wrapper.sigil_slots, 1)

    def test_set_sigil(self):
        # given
        item: Item = build_weapon()
        wrapper: SigilWrapper = SigilWrapper(item)
        sigil: Item = build_sigil()

        # when
        wrapper.set_sigil(sigil, 0)

        # then
        assert_weapon(self, wrapper, item)
        assert_sigil(self, wrapper.get_sigils()[0], sigil)

    def test_set_multiple_sigil(self):
        # given
        item: Item = build_weapon(type=WeaponType.LongBow)
        wrapper: SigilWrapper = SigilWrapper(item)
        sigil1: Item = build_sigil(id=1)
        sigil2: Item = build_sigil(id=2)

        # when
        wrapper.set_sigil(sigil1, 0)
        wrapper.set_sigil(sigil2, 1)

        # then
        assert_weapon(self, wrapper, item)
        sigils = wrapper.get_sigils()
        assert_sigil(self, sigils[0], sigil1)
        assert_sigil(self, sigils[1], sigil2)
