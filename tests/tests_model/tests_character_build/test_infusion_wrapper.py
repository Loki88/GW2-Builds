#!/usr/bin/env python

import unittest

from model.api import Item
from model.characted_build import InfusionWrapper
from tests.test_utils import build_infusion, build_weapon, assert_infusion, assert_weapon


class TestInfusionWrapper(unittest.TestCase):

    def test_access_fields(self):
        # given
        item: Item = build_weapon()

        # when
        wrapper: InfusionWrapper = InfusionWrapper(item)

        # then
        assert_weapon(self, wrapper, item)
        self.assertEqual(wrapper.infusion_slots, 1)

    def test_set_infusion(self):
        # given
        item: Item = build_weapon()
        wrapper: InfusionWrapper = InfusionWrapper(item)
        infusion: Item = build_infusion()

        # when
        wrapper.set_infusion(infusion, 0)

        # then
        assert_weapon(self, wrapper, item)
        assert_infusion(self, wrapper.get_infusions()[0], infusion)

    def test_set_multiple_infusion(self):
        # given
        item: Item = build_weapon(slots=2)
        wrapper: InfusionWrapper = InfusionWrapper(item)
        infusion1: Item = build_infusion(id=1)
        infusion2: Item = build_infusion(id=2)

        # when
        wrapper.set_infusion(infusion1, 0)
        wrapper.set_infusion(infusion2, 1)

        # then
        assert_weapon(self, wrapper, item)
        infusions = wrapper.get_infusions()
        assert_infusion(self, infusions[0], infusion1)
        assert_infusion(self, infusions[1], infusion2)
