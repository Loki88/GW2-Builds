#!/usr/bin/env python

from enum import Enum


class Attribute(Enum):
    CritDamage = 0 # Ferocity
    Healing = 1
    Power = 2
    Precision = 3
    Toughness = 4
    Vitality = 5
    Concentration = 6
    ConditionDamage = 7
    Expertise = 8
    
class Condition(Enum):
    Vulnerability = 0
    Bleeding = 1
    Burning = 2
    Confusion = 3
    Poisoned = 4
    Torment = 5
    Crowd = 6
    Blinded = 7
    Chilled = 8
    Crippled = 9
    Fear = 10
    Immobile = 11
    Slow = 12
    Taunt = 13
    Weakness = 14
    Other = 15
    
class Boon(Enum):
    Aegis = 0
    Alacrity = 1
    Fury = 2
    Might = 3
    Protection = 4
    Quickness = 5
    Regeneration = 6
    Resistance = 7
    Resolution = 8
    Stability = 9
    Swiftness = 10
    Vigor = 11
    
class ControlEffect(Enum):
    Daze = 0
    Stun = 1
    Knockdown = 2
    Pull = 3
    Knockback = 4
    Launch = 5
    Float = 6
    Sink = 7
    Fear = 8
    Taunt = 9

class FieldType(Enum):
    Air = 0
    Dark = 1
    Fire = 2
    Ice = 3
    Light = 4
    Lightning = 5
    Poison = 6
    Smoke = 7
    Ethereal = 8
    Water = 9
    
class FinisherType(Enum):
    Blast = 0
    Leap = 1
    Projectile = 2
    Whirl = 3
    
class FactType(Enum):
    AttributeAdjust = 0
    Buff = 1
    BuffConversion = 2
    ComboField = 3
    ComboFinisher = 4
    Damage = 5
    Distance = 6
    NoData = 7
    Number = 8
    Percent = 9
    PrefixedBuff = 10
    Radius = 11
    Range = 12
    Recharge = 13
    Time = 14
    Unblockable = 15

class Stats(Enum):
    pass