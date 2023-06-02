#!/usr/bin/env python

from enum import Enum


class Attribute(Enum):
    CritDamage = 0  # Ferocity
    Healing = 1
    Power = 2
    Precision = 3
    Toughness = 4
    Vitality = 5
    BoonDuration = 6
    ConditionDamage = 7
    ConditionDuration = 8
    AgonyResistance = 9


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


class SkillType(Enum):
    Bundle = 0  # Used for Engineer kits or weapons picked up in-world.
    Elite = 1  # Elite skill.
    Heal = 2  # Heal skill.
    Monster = 3  # Used for some NPC skills.
    Pet = 4  # Used for Ranger pet skills.
    # Profession-specific skill, such as Elementalist attunements or Engineer toolbelt skills.
    Profession = 5
    Toolbelt = 6  # Used for some Engineer toolbelt skills.
    Transform = 7  # Placeholder skill used to indicate a locked slot.
    Utility = 8  # Utility skill.
    Weapon = 9  # Weapon skill or downed skill.


class Slot(Enum):
    Downed_1 = 0  # Downed skills 1-4
    Downed_2 = 1
    Downed_3 = 2
    Downed_4 = 3
    Pet = 4  # Used for Ranger pet skills
    Profession_1 = 5  # Profession skills 1-5
    Profession_2 = 6
    Profession_3 = 7
    Profession_4 = 8
    Profession_5 = 9
    Utility = 10  # Utility skill
    Weapon_1 = 11  # Weapon skills 1-5
    Weapon_2 = 12
    Weapon_3 = 13
    Weapon_4 = 14
    Weapon_5 = 15
    Elite = 16


class SkillCategory(Enum):
    # Indicates the skill is a dual-wield skill for thieves. The necessary off-hand weapon is indicated in dual_wield.
    DualWield = 0
    # Indicates the skill can only be used by a thief in stealth.
    StealthAttack = 1
    # All other values of this field simply indicate which group of skills it belongs to. (i.e. Signet, Cantrip, etc.)
    Others = 2


class SkillFlag(Enum):
    GroundTargeted = 0
    NoUnderwater = 1


class ConsumableType(Enum):
    Food = 0
    Utility = 1


class ArmorType(Enum):
    Boots = 0
    Coat = 1
    Gloves = 2
    Helm = 3
    HelmAquatic = 4
    Leggings = 5
    Shoulders = 6


class ArmorWeight(Enum):
    Heavy = 0
    Medium = 1
    Light = 2


class ItemRarity(Enum):
    Legendary = 0
    Ascended = 1


class TrinketType(Enum):
    Accessory = 0
    Amulet = 1
    Ring = 2


class UpgradeComponentType(Enum):
    Default = 0  # Infusions and Jewels (and historical PvP runes/sigils)
    Gem = 1  # Universal upgrades (Gemstones, Doubloons, and Marks/Crests/etc.)
    Rune = 2  # Rune
    Sigil = 3  # Sigil


class UpgradeComponentFlags(Enum):
    Weapons = 0
    Armor = 1
    Trinkets = 2


class ItemType(Enum):
    Armor = 0
    Back = 1
    Trinket = 2
    Consumable = 3
    UpgradeComponent = 4
    Weapon = 5


class WeaponType(Enum):
    Axe = 0
    Dagger = 1
    Mace = 2
    Pistol = 3
    Scepter = 4
    Sword = 5
    Focus = 6
    Shield = 7
    Torch = 8
    Warhorn = 9
    Greatsword = 10
    Hammer = 11
    LongBow = 12
    Rifle = 13
    ShortBow = 14
    Staff = 15
    Harpoon = 16
    Speargun = 17
    Trident = 18
    LargeBundle = 19
    SmallBundle = 20
    Toy = 21
    ToyTwoHanded = 22


class DamageType(Enum):
    Fire = 0
    Ice = 1
    Lightning = 2
    Physical = 3
    Choking = 4


class InfusionFlag(Enum):
    Enrichment = 0  # Item has an enrichment slot.
    Infusion = 1  # Item has an infusion slot.


class TraitSlot(Enum):
    Major = 0
    Minor = 1
