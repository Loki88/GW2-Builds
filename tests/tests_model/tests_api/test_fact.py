#!/usr/bin/env python

import unittest

from model.api.fact import *
from model.api.enums import FactType, Attribute, Condition, Boon, ControlEffect


class TestFact(unittest.TestCase):

    def test_attribute_adjust(self):
        # given
        data = {
            'text': 'test text',
            'icon': 'test icon',
            'type': FactType.AttributeAdjust.name,
            'target': Attribute.CritDamage.name,
            'value': 140
        }

        # when
        fact = get_fact(data)

        # then
        self.assertIsNotNone(fact)
        self.assertTrue(isinstance(fact, AttributeAdjust))
        self.assertEqual(fact.text, 'test text')
        self.assertEqual(fact.icon, 'test icon')
        self.assertEqual(fact.type, FactType.AttributeAdjust)
        self.assertEqual(fact.target, Attribute.CritDamage)
        self.assertEqual(fact.value, 140)

    def test_buff_condition(self):
        # given
        data = {
            'text': 'test text',
            'icon': 'test icon',
            'type': FactType.Buff.name,
            'duration': 5,
            'status': Condition.Bleeding.name
        }

        # when
        fact = get_fact(data)

        # then
        self.assertIsNotNone(fact)
        self.assertTrue(isinstance(fact, Buff))
        self.assertEqual(fact.text, 'test text')
        self.assertEqual(fact.icon, 'test icon')
        self.assertEqual(fact.type, FactType.Buff)
        self.assertEqual(fact.status, Condition.Bleeding)

    def test_buff_boon(self):
        # given
        data = {
            'text': 'test text',
            'icon': 'test icon',
            'type': FactType.Buff.name,
            'duration': 5,
            'status': Boon.Alacrity.name
        }

        # when
        fact = get_fact(data)

        # then
        self.assertIsNotNone(fact)
        self.assertTrue(isinstance(fact, Buff))
        self.assertEqual(fact.text, 'test text')
        self.assertEqual(fact.icon, 'test icon')
        self.assertEqual(fact.type, FactType.Buff)
        self.assertEqual(fact.status, Boon.Alacrity)

    def test_buff_control_effect(self):
        # given
        data = {
            'text': 'test text',
            'icon': 'test icon',
            'type': FactType.Buff.name,
            'duration': 5,
            'status': ControlEffect.Stun.name
        }

        # when
        fact = get_fact(data)

        # then
        self.assertIsNotNone(fact)
        self.assertTrue(isinstance(fact, Buff))
        self.assertEqual(fact.text, 'test text')
        self.assertEqual(fact.icon, 'test icon')
        self.assertEqual(fact.type, FactType.Buff)
        self.assertEqual(fact.status, ControlEffect.Stun)

    def test_buff_conversion(self):
        # given
        data = {
            'text': 'test text',
            'icon': 'test icon',
            'type': FactType.BuffConversion.name,
            'target': Attribute.CritDamage.name,
            'source': Attribute.BoonDuration.name,
            'percent': 15.7
        }

        # when
        fact = get_fact(data)

        # then
        self.assertIsNotNone(fact)
        self.assertTrue(isinstance(fact, BuffConversion))
        self.assertEqual(fact.text, 'test text')
        self.assertEqual(fact.icon, 'test icon')
        self.assertEqual(fact.type, FactType.BuffConversion)
        self.assertEqual(fact.target, Attribute.CritDamage)
        self.assertEqual(fact.source, Attribute.BoonDuration)
        self.assertEqual(fact.percent, 15.7)

    def test_combo_field(self):
        # given
        data = {
            'text': 'test text',
            'icon': 'test icon',
            'type': FactType.ComboField.name,
            'field_type': FieldType.Dark.name
        }

        # when
        fact = get_fact(data)

        # then
        self.assertIsNotNone(fact)
        self.assertTrue(isinstance(fact, ComboField))
        self.assertEqual(fact.text, 'test text')
        self.assertEqual(fact.icon, 'test icon')
        self.assertEqual(fact.type, FactType.ComboField)
        self.assertEqual(fact.field_type, FieldType.Dark)

    def test_combo_finisher(self):
        # given
        data = {
            'text': 'test text',
            'icon': 'test icon',
            'type': FactType.ComboFinisher.name,
            'finisher_type': FinisherType.Blast.name,
            'percent': 63.2
        }

        # when
        fact = get_fact(data)

        # then
        self.assertIsNotNone(fact)
        self.assertTrue(isinstance(fact, ComboFinisher))
        self.assertEqual(fact.text, 'test text')
        self.assertEqual(fact.icon, 'test icon')
        self.assertEqual(fact.type, FactType.ComboFinisher)
        self.assertEqual(fact.finisher_type, FinisherType.Blast)
        self.assertEqual(fact.percent, 63.2)

    def test_damage(self):
        # given
        data = {
            'text': 'test text',
            'icon': 'test icon',
            'type': FactType.Damage.name,
            'hit_count': 5
        }

        # when
        fact = get_fact(data)

        # then
        self.assertIsNotNone(fact)
        self.assertTrue(isinstance(fact, Damage))
        self.assertEqual(fact.text, 'test text')
        self.assertEqual(fact.icon, 'test icon')
        self.assertEqual(fact.type, FactType.Damage)
        self.assertEqual(fact.hit_count, 5)

    def test_distance(self):
        # given
        data = {
            'text': 'test text',
            'icon': 'test icon',
            'type': FactType.Distance.name,
            'distance': 300
        }

        # when
        fact = get_fact(data)

        # then
        self.assertIsNotNone(fact)
        self.assertTrue(isinstance(fact, Distance))
        self.assertEqual(fact.text, 'test text')
        self.assertEqual(fact.icon, 'test icon')
        self.assertEqual(fact.type, FactType.Distance)
        self.assertEqual(fact.distance, 300)

    def test_no_data(self):
        # given
        data = {
            'text': 'test text',
            'icon': 'test icon',
            'type': FactType.NoData.name
        }

        # when
        fact = get_fact(data)

        # then
        self.assertIsNotNone(fact)
        self.assertTrue(isinstance(fact, NoData))
        self.assertEqual(fact.text, 'test text')
        self.assertEqual(fact.icon, 'test icon')
        self.assertEqual(fact.type, FactType.NoData)

    def test_number(self):
        # given
        data = {
            'text': 'test text',
            'icon': 'test icon',
            'type': FactType.Number.name,
            'value': 23
        }

        # when
        fact = get_fact(data)

        # then
        self.assertIsNotNone(fact)
        self.assertTrue(isinstance(fact, Number))
        self.assertEqual(fact.text, 'test text')
        self.assertEqual(fact.icon, 'test icon')
        self.assertEqual(fact.type, FactType.Number)
        self.assertEqual(fact.value, 23)

    def test_percent(self):
        # given
        data = {
            'text': 'test text',
            'icon': 'test icon',
            'type': FactType.Percent.name,
            'percent': 23.5
        }

        # when
        fact = get_fact(data)

        # then
        self.assertIsNotNone(fact)
        self.assertTrue(isinstance(fact, Percent))
        self.assertEqual(fact.text, 'test text')
        self.assertEqual(fact.icon, 'test icon')
        self.assertEqual(fact.type, FactType.Percent)
        self.assertEqual(fact.percent, 23.5)

    def test_prefixed_buff(self):
        # given
        data = {
            'text': 'test text',
            'icon': 'test icon',
            'type': FactType.PrefixedBuff.name,
            'duration': 5,
            'status': Condition.Bleeding.name,
            'prefix': {
                'text': 'prefix text',
                'icon': 'prefix icon',
                'status': 'prefix status',
                'description': 'prefix description'
            }
        }

        # when
        fact = get_fact(data)

        # then
        self.assertIsNotNone(fact)
        self.assertTrue(isinstance(fact, PrefixedBuff))
        self.assertEqual(fact.text, 'test text')
        self.assertEqual(fact.icon, 'test icon')
        self.assertEqual(fact.type, FactType.PrefixedBuff)
        self.assertEqual(fact.status, Condition.Bleeding)
        self.assertIsNotNone(fact.prefix)
        self.assertTrue(isinstance(fact.prefix, BuffPrefix))
        self.assertEqual(fact.prefix.text, 'prefix text')
        self.assertEqual(fact.prefix.icon, 'prefix icon')
        self.assertEqual(fact.prefix.status, 'prefix status')
        self.assertEqual(fact.prefix.description, 'prefix description')

    def test_radius(self):
        # given
        data = {
            'text': 'test text',
            'icon': 'test icon',
            'type': FactType.Radius.name,
            'distance': 300
        }

        # when
        fact = get_fact(data)

        # then
        self.assertIsNotNone(fact)
        self.assertTrue(isinstance(fact, Radius))
        self.assertEqual(fact.text, 'test text')
        self.assertEqual(fact.icon, 'test icon')
        self.assertEqual(fact.type, FactType.Radius)
        self.assertEqual(fact.distance, 300)

    def test_range(self):
        # given
        data = {
            'text': 'test text',
            'icon': 'test icon',
            'type': FactType.Range.name,
            'value': 23
        }

        # when
        fact = get_fact(data)

        # then
        self.assertIsNotNone(fact)
        self.assertTrue(isinstance(fact, Range))
        self.assertEqual(fact.text, 'test text')
        self.assertEqual(fact.icon, 'test icon')
        self.assertEqual(fact.type, FactType.Range)
        self.assertEqual(fact.value, 23)

    def test_recharge(self):
        # given
        data = {
            'text': 'test text',
            'icon': 'test icon',
            'type': FactType.Recharge.name,
            'value': 23
        }

        # when
        fact = get_fact(data)

        # then
        self.assertIsNotNone(fact)
        self.assertTrue(isinstance(fact, Recharge))
        self.assertEqual(fact.text, 'test text')
        self.assertEqual(fact.icon, 'test icon')
        self.assertEqual(fact.type, FactType.Recharge)
        self.assertEqual(fact.value, 23)

    def test_time(self):
        # given
        data = {
            'text': 'test text',
            'icon': 'test icon',
            'type': FactType.Time.name,
            'duration': 3.4
        }

        # when
        fact = get_fact(data)

        # then
        self.assertIsNotNone(fact)
        self.assertTrue(isinstance(fact, Time))
        self.assertEqual(fact.text, 'test text')
        self.assertEqual(fact.icon, 'test icon')
        self.assertEqual(fact.type, FactType.Time)
        self.assertEqual(fact.duration, 3.4)

    def test_unblockable(self):
        # given
        data = {
            'text': 'test text',
            'icon': 'test icon',
            'type': FactType.Unblockable.name,
            'value': True
        }

        # when
        fact = get_fact(data)

        # then
        self.assertIsNotNone(fact)
        self.assertTrue(isinstance(fact, Unblockable))
        self.assertEqual(fact.text, 'test text')
        self.assertEqual(fact.icon, 'test icon')
        self.assertEqual(fact.type, FactType.Unblockable)
        self.assertTrue(fact.value)
