#!/usr/bin/env python

import unittest

from model.api import Item, ItemStats
from model.characted_build import StatsWrapper
from tests.test_utils import build_stats, build_armor, assert_stats, assert_armor


class TestRuneWrapper(unittest.TestCase):

    def test_access_fields(self):
        # given
        item: Item = build_armor()

        # when
        wrapper: StatsWrapper = StatsWrapper(item)

        # then
        assert_armor(self, wrapper, item)

    def test_set_stats(self):
        # given
        item: Item = build_armor()
        wrapper: StatsWrapper = StatsWrapper(item)
        stats: ItemStats = build_stats()

        # when
        wrapper.set_stats(stats)

        # then
        assert_armor(self, wrapper, item)
        assert_stats(self, wrapper.get_stats(), stats)
