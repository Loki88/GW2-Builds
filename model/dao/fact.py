#!/usr/bin/env python

import persistent
from model import Attribute, Condition, Boon, ControlEffect, FieldType, FinisherType, FactType


class Fact(persistent.Persistent):

    def __init__(self, text: str, icon: str, type: FactType) -> None:
        super.__init__()
        self.text = text
        self.icon = icon
        self.type = type


class TargetedFact(Fact):

    def __init__(self, text: str, icon: str, type: FactType, target: Attribute) -> None:
        super().__init__(text, icon, type)
        self.target = target


class AttributeAdjust(TargetedFact):

    def __init__(self, text: str, icon: str, type: FactType, target: Attribute, value: int) -> None:
        super().__init__(text, icon, type, target)
        self.value = value


class Buff(Fact):

    def __init__(self, text: str, icon: str, type: FactType,
                 duration: float, status: Condition | Boon | ControlEffect, description: str, apply_count: int) -> None:
        super().__init__(text, icon, type)

        self.duration = duration
        self.status = status
        self.description = description
        self.apply_count = apply_count


class BuffConversion(TargetedFact):

    def __init__(self, text: str, icon: str, type: FactType, target: Attribute,
                 source: Attribute, percent: float) -> None:
        super().__init__(text, icon, type, target)
        self.source = source
        self.percent = percent


class ComboField(Fact):

    def __init__(self, text: str, icon: str, type: FactType,
                 field_type: FieldType) -> None:
        super().__init__(text, icon, type)
        self.field_type = field_type


class ComboFinisher(Fact):

    def __init__(self, text: str, icon: str, type: FactType,
                 finisher_type: FinisherType, percent: float) -> None:
        super().__init__(text, icon, type)
        self.finisher_type = finisher_type
        self.percent = percent


class Damage(Fact):

    def __init__(self, text: str, icon: str, type: FactType,
                 hit_count: int) -> None:
        super().__init__(text, icon, type)
        self.hit_count = hit_count


class Distance(Fact):

    def __init__(self, text: str, icon: str, type: FactType,
                 distance: int) -> None:
        super().__init__(text, icon, type)
        self.distance = distance


class NoData(Fact):
    pass


class Number(Fact):

    def __init__(self, text: str, icon: str, type: FactType,
                 value: int) -> None:
        super().__init__(text, icon, type)
        self.value = value


class Percent(Fact):

    def __init__(self, text: str, icon: str, type: FactType,
                 percent: float) -> None:
        super().__init__(text, icon, type)
        self.percent = percent


class BuffPrefix(persistent.Persistent):

    def __init__(self, text: str, icon: str, status: str, description: str) -> None:
        self.text = text
        self.icon = icon
        self.status = status
        self.description = description


class PrefixedBuff(Buff):

    def __init__(self, text: str, icon: str, type: FactType,
                 duration: float, status: Condition | Boon | ControlEffect, description: str, apply_count: int,
                 prefix: BuffPrefix) -> None:
        super().__init__(text, icon, type, duration, status, description, apply_count)
        self.prefix = prefix


class Radius(Distance):
    pass


class Range(Number):
    pass


class Recharge(Number):
    pass


class Time(Fact):

    def __init__(self, text: str, icon: str, type: FactType,
                 duration: float) -> None:
        super().__init__(text, icon, type)
        self.duration = duration


class Unblockable(Fact):

    def __init__(self, text: str, icon: str, type: FactType,
                 value: bool) -> None:
        super().__init__(text, icon, type)
        self.value = value

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


def get_fact(fact_type: FactType, **kwargs) -> Fact | None:
    constructor = FACTS_DICT[fact_type]
    return constructor(kwargs)
