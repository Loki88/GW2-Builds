#!/usr/bin/env python

from .utils import get_or_none
from .enums import Attribute, Condition, Boon, ControlEffect, FieldType, FinisherType, FactType

class Fact:
    text: str
    icon: str
    type: FactType
    
    def __init__(self, data: dict = None) -> None:
        if(data is not None):
            self.text = get_or_none('text', data)
            self.icon = get_or_none('icon', data)
            self.type = FactType[get_or_none('type', data)]
    
    # fact requires a strategy and a hierarchy of facts to represent the different facts
    
class TargetedFact(Fact):
    target: Attribute
    
    def __init__(self, data: dict = None) -> None:
        super().__init__(data)
        if(data is not None):
            self.target = Attribute[get_or_none('target', data)]
    
    
class AttributeAdjust(TargetedFact):
    value: int
    
    def __init__(self, data: dict = None) -> None:
        super().__init__(data)
        if(data is not None):
            self.value = get_or_none('value', data)

class Buff(Fact):
    duration: float
    status: Condition | Boon | ControlEffect
    description: str
    apply_count: int
    
    def __init__(self, data: dict = None) -> None:
        super().__init__(data)
        if(data is not None):
            self.duration = get_or_none('duration', data)
            self.status = self._compute_status(get_or_none('status', data))
            self.description = get_or_none('description', data)
            self.apply_count = get_or_none('apply_count', data)
            
    def _compute_status(self, value: str) -> Condition | Boon | ControlEffect:
        if(value is not None):
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
    source: Attribute
    percent: float
    
    def __init__(self, data: dict = None) -> None:
        super().__init__(data)
        if(data is not None):
            self.source = Attribute[get_or_none('source', data)]
            self.percent = get_or_none('percent', data)
    
class ComboField(Fact):
    field_type: FieldType
    
    def __init__(self, data: dict = None) -> None:
        super().__init__(data)
        if(data is not None):
            self.field_type = FieldType[get_or_none('field_type', data)]

class ComboFinisher(Fact):
    finisher_type: FinisherType
    percent: float
    
    def __init__(self, data: dict = None) -> None:
        super().__init__(data)
        if(data is not None):
            self.finisher_type = FinisherType[get_or_none('finisher_type', data)]
            self.percent = get_or_none('percent', data)

class Damage(Fact):
    hit_count: int
    
    def __init__(self, data: dict = None) -> None:
        super().__init__(data)
        if(data is not None):
            self.hit_count = get_or_none('hit_count', data)

class Distance(Fact):
    distance: int
    
    def __init__(self, data: dict = None) -> None:
        super().__init__(data)
        if(data is not None):
            self.distance = get_or_none('distance', data)

class NoData(Fact):
    pass

class Number(Fact):
    value: int
    
    def __init__(self, data: dict = None) -> None:
        super().__init__(data)
        if(data is not None):
            self.value = get_or_none('value', data)

class Percent(Fact):
    percent: float
    
    def __init__(self, data: dict = None) -> None:
        super().__init__(data)
        if(data is not None):
            self.percent = get_or_none('percent', data)
            
class BuffPrefix:
    text: str
    icon: str
    status: str
    description: str
    
    def __init__(self, data: dict = None) -> None:
        if(data is not None):
            self.text = get_or_none('text', data)
            self.icon = get_or_none('icon', data)
            self.status = get_or_none('status', data)
            self.description = get_or_none('description', data)
    

class PrefixedBuff(Buff):
    prefix: BuffPrefix
    
    def __init__(self, data: dict = None) -> None:
        super().__init__(data)
        if(data is not None):
            self.prefix = BuffPrefix(get_or_none('prefix', data))
    
class Radius(Distance):
    pass
    
class Range(Number):
    pass    
    
class Recharge(Number):
    pass    
    
class Time(Fact):
    duration: float
    
    def __init__(self, data: dict = None) -> None:
        super().__init__(data)
        if(data is not None):
            self.duration = get_or_none('duration', data)
          
    
class Unblockable(Fact):
    value: bool
    
    def __init__(self, data: dict = None) -> None:
        super().__init__(data)
        if(data is not None):
            self.value = get_or_none('value', data)      

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
    if(data is not None):
        fact_type = FactType[data['type']]
        constructor = FACTS_DICT[fact_type]
        return constructor(data)
    else:
        return None
