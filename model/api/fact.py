#!/usr/bin/env python

from typing import Callable
from abc import ABC, abstractmethod
from .api_decorator import ApiDecorator
from model.enums import Attribute, Condition, Boon, ControlEffect, FieldType, FinisherType, FactType


class Fact(ApiDecorator, ABC):

    def __init__(self, data: dict = None,
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = [],
                 converters: dict[str, Callable] = {}) -> None:
        super().__init__(data,
                         attributes + ['text', 'icon', 'type'],
                         list_attributes,
                         dict_attributes,
                         {
                             'type': lambda x: FactType[x] if x is not None else None
                         }
                         | converters)


class TargetedFact(Fact, ABC):

    def __init__(self, data: dict = None,
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = [],
                 converters: dict[str, Callable] = {}) -> None:
        super().__init__(data,
                         attributes + ['target'],
                         list_attributes,
                         dict_attributes,
                         {
                             'target': lambda x: Attribute[x] if x is not None else None
                         }
                         | converters)


class AttributeAdjust(TargetedFact):

    def __init__(self, data: dict = None,
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = [],
                 converters: dict[str, Callable] = {}) -> None:
        super().__init__(data,
                         attributes + ['value'],
                         list_attributes,
                         dict_attributes,
                         converters)


class Buff(Fact):

    def __init__(self, data: dict = None,
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = [],
                 converters: dict[str, Callable] = {}) -> None:
        super().__init__(data,
                         attributes + ['duration', 'status',
                                       'description', 'apply_count'],
                         list_attributes,
                         dict_attributes,
                         {
                             'status': lambda x: self._compute_status(x) if x is not None else None
                         }
                         | converters)

    def _compute_status(self, value: str) -> Condition | Boon | ControlEffect:
        if (value is not None):
            if value in Condition._member_names_:
                return Condition[value]
            elif value in Boon._member_names_:
                return Boon[value]
            elif value in ControlEffect._member_names_:
                return ControlEffect[value]
            else:
                return None
        else:
            return None


class BuffConversion(TargetedFact):

    def __init__(self, data: dict = None,
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = [],
                 converters: dict[str, Callable] = {}) -> None:
        super().__init__(data,
                         attributes + ['source', 'percent'],
                         list_attributes,
                         dict_attributes,
                         {
                             'source': lambda x: Attribute[x] if x is not None else None
                         }
                         | converters)


class ComboField(Fact):

    def __init__(self, data: dict = None,
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = [],
                 converters: dict[str, Callable] = {}) -> None:
        super().__init__(data,
                         attributes + ['field_type'],
                         list_attributes,
                         dict_attributes,
                         {
                             'field_type': lambda x: FieldType[x] if x is not None else None
                         }
                         | converters)


class ComboFinisher(Fact):

    def __init__(self, data: dict = None,
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = [],
                 converters: dict[str, Callable] = {}) -> None:
        super().__init__(data,
                         attributes + ['finisher_type', 'percent'],
                         list_attributes,
                         dict_attributes,
                         {
                             'finisher_type': lambda x: FinisherType[x] if x is not None else None
                         }
                         | converters)


class Damage(Fact):

    def __init__(self, data: dict = None,
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = [],
                 converters: dict[str, Callable] = {}) -> None:
        super().__init__(data,
                         attributes + ['hit_count'],
                         list_attributes,
                         dict_attributes,
                         converters)


class Distance(Fact):

    def __init__(self, data: dict = None,
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = [],
                 converters: dict[str, Callable] = {}) -> None:
        super().__init__(data,
                         attributes + ['distance'],
                         list_attributes,
                         dict_attributes,
                         converters)


class NoData(Fact):
    pass


class Number(Fact):

    def __init__(self, data: dict = None,
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = [],
                 converters: dict[str, Callable] = {}) -> None:
        super().__init__(data,
                         attributes + ['value'],
                         list_attributes,
                         dict_attributes,
                         converters)


class Percent(Fact):

    def __init__(self, data: dict = None,
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = [],
                 converters: dict[str, Callable] = {}) -> None:
        super().__init__(data,
                         attributes + ['percent'],
                         list_attributes,
                         dict_attributes,
                         converters)


class BuffPrefix(ApiDecorator):

    def __init__(self, data: dict = None,
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = [],
                 converters: dict[str, Callable] = {}) -> None:
        super().__init__(data,
                         attributes + ['text', 'icon',
                                       'status', 'description'],
                         list_attributes,
                         dict_attributes,
                         converters)


class PrefixedBuff(Buff):

    def __init__(self, data: dict = None,
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = [],
                 converters: dict[str, Callable] = {}) -> None:
        super().__init__(data,
                         attributes + ['prefix'],
                         list_attributes,
                         dict_attributes,
                         {
                             'prefix': lambda x: BuffPrefix(x) if x is not None else None
                         }
                         | converters)


class Radius(Distance):
    pass


class Range(Number):
    pass


class Recharge(Number):
    pass


class Time(Fact):

    def __init__(self, data: dict = None,
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = [],
                 converters: dict[str, Callable] = {}) -> None:
        super().__init__(data,
                         attributes + ['duration'],
                         list_attributes,
                         dict_attributes,
                         converters)


class Unblockable(Fact):

    def __init__(self, data: dict = None,
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = [],
                 converters: dict[str, Callable] = {}) -> None:
        super().__init__(data,
                         attributes + ['value'],
                         list_attributes,
                         dict_attributes,
                         converters)

# Factory for facts


FACTS_DICT: dict = {
    FactType.AttributeAdjust: AttributeAdjust,
    FactType.Buff: Buff,
    FactType.BuffConversion: BuffConversion,
    FactType.ComboField: ComboField,
    FactType.ComboFinisher: ComboFinisher,
    FactType.Damage: Damage,
    FactType.Distance: Distance,
    FactType.NoData: NoData,
    FactType.Number: Number,
    FactType.Percent: Percent,
    FactType.PrefixedBuff: PrefixedBuff,
    FactType.Radius: Radius,
    FactType.Range: Range,
    FactType.Recharge: Recharge,
    FactType.Time: Time,
    FactType.Unblockable: Unblockable
}


def get_fact(data: dict = None) -> Fact | None:
    if (data is not None):
        fact_type = FactType[data['type']]
        constructor = FACTS_DICT[fact_type]
        return constructor(data)
    else:
        return None
