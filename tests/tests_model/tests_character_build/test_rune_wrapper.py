#!/usr/bin/env python

import unittest

from model.api import Item
from model.characted_build import RuneWrapper
from tests.test_utils import build_rune, build_armor, assert_rune, assert_armor


class TestRuneWrapper(unittest.TestCase):

    def test_access_fields(self):
        # given
        item: Item = build_armor()

        # when
        wrapper: RuneWrapper = RuneWrapper(item)

        # then
        assert_armor(self, wrapper, item)

    def test_set_rune(self):
        # given
        item: Item = build_armor()
        wrapper: RuneWrapper = RuneWrapper(item)
        rune: Item = build_rune()

        # when
        wrapper.set_rune(rune)

        # then
        assert_armor(self, wrapper, item)
        assert_rune(self, wrapper.get_rune(), rune)
