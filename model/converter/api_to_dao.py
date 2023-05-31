
from ..api import Profession as ProfessionAPI, Weapon as WeaponAPI, Skill as SkillAPI, Fact as FactAPI, FactType,\
    Specialization as SpecializationAPI, Trait as TraitAPI, ItemStats as ItemStatsAPI, AttributeBonus as AttributeBonusAPI,\
    Item as ItemAPI, ItemType, ItemDetail as ItemDetailAPI
from ..dao import Profession as ProfessionDao, Weapon as WeaponDao, Skill as SkillDao, Fact as FactDao,\
    AttributeAdjust as AttributeAdjustDao, Buff as BuffDao, BuffConversion as BuffConversionDao, ComboField as ComboFieldDao,\
    ComboFinisher as ComboFinisherDao, Damage as DamageDao, Distance as DistanceDao, NoData as NoDataDao, Number as NumberDao,\
    Percent as PercentDao, PrefixedBuff as PrefixedBuffDao, Radius as RadiusDao, Range as RangeDao, Recharge as RechargeDao,\
    Time as TimeDao, Unblockable as UnblockableDao, Specialization as SpecializationDao, Trait as TraitDao, ItemStats as ItemStatsDao,\
    AttributeBonus as AttributeBonusDao, Item as ItemDao, ItemDetail as ItemDetailDao, get_item_details


T_CONVERTER = {
    FactType.AttributeAdjust: lambda x: AttributeAdjustDao(x.text, x.icon, x.type, x.target, x.value),
    FactType.Buff: lambda x: BuffDao(x.text, x.icon, x.type, x.duration, x.status, x.description, x.apply_count),
    FactType.BuffConversion: lambda x: BuffConversionDao(x.text, x.icon, x.type,  x.target, x.source, x.percent),
    FactType.ComboField: lambda x: ComboFieldDao(x.text, x.icon, x.type, x.field_type),
    FactType.ComboFinisher: lambda x: ComboFinisherDao(x.text, x.icon, x.type, x.finisher_type, x.percent),
    FactType.Damage: lambda x: DamageDao(x.text, x.icon, x.type, x.hit_count),
    FactType.Distance: lambda x: DistanceDao(x.text, x.icon, x.type, x.distance),
    FactType.NoData: lambda x: NoDataDao(x.text, x.icon, x.type),
    FactType.Number: lambda x: NumberDao(x.text, x.icon, x.type, x.value),
    FactType.Percent: lambda x: PercentDao(x.text, x.icon, x.type, x.percent),
    FactType.PrefixedBuff: lambda x: PrefixedBuffDao(x.text, x.icon, x.type, x.duration, x.status, x.description, x.apply_count, x.prefix),
    FactType.Radius: lambda x: RadiusDao(x.text, x.icon, x.type, x.distance),
    FactType.Range: lambda x: RangeDao(x.text, x.icon, x.type, x.value),
    FactType.Recharge: lambda x: RechargeDao(x.text, x.icon, x.type, x.value),
    FactType.Time: lambda x: TimeDao(x.text, x.icon, x.type, x.duration),
    FactType.Unblockable: lambda x: UnblockableDao(
        x.text, x.icon, x.type, x.value)
}


def convert_fact(api: FactAPI) -> FactDao:
    return T_CONVERTER(api.type)(api)


def convert_skill(api: SkillAPI) -> SkillDao:
    dao = SkillDao(id=api.id, name=api.name, description=api.description, icon=api.icon, chat_link=api.chat_link,
                   type=api.type, weapon_type=api.weapon_type, slot=api.slot, attunement=api.attunement,
                   cost=api.cost, dual_wield=api.dual_wield, flip_skill=api.flip_skill, initiative=api.initiative,
                   next_chain=api.next_chain, prev_chain=api.prev_chain)

    for skill in api.bundle_skills:
        dao.add_boundle_skill(skill)

    for cat in api.categories:
        dao.add_category(cat)

    for fact in api.facts:
        dao.add_fact(convert_fact(fact))

    for flag in api.flags:
        dao.add_flag(flag)

    for profession in api.professions:
        dao.add_profession(profession)

    for skill in api.toolbelt_skill:
        dao.add_toolbelt_skill(skill)

    for fact in api.traited_facts:
        dao.add_traited_fact(convert_fact(fact))

    for skill in api.transform_skills:
        dao.add_transform_skill(skill)


def convert_weapon(api: WeaponAPI) -> WeaponDao:
    dao = WeaponDao(name=api.name, specialization=api.specialization)

    for skill in api.skills:
        dao.add_skill(skill)


def convert_profession(api: ProfessionAPI) -> ProfessionDao:
    dao = ProfessionDao(id=api.id, name=api.name, code=api.code,
                        icon=api.icon, icon_big=api.icon_big)

    for spec in api.specializations:
        dao.add_specialization(spec)

    for flag in api.flags:
        dao.add_flag(flag)

    for weapon in api.weapons:
        dao.add_weapon(convert_weapon(weapon))


def convert_specialization(api: SpecializationAPI) -> SpecializationDao:
    dao = SpecializationDao(id=api.id, name=api.name, profession=api.profession,
                            elite=api.elite, icon=api.icon, background=api.background)

    for trait in api.major_traits:
        dao.add_major_trait(trait)

    for trait in api.minor_traits:
        dao.add_minor_trait(trait)


def convert_trait(api: TraitAPI) -> TraitDao:
    dao = TraitDao(id=api.id, name=api.name, icon=api.icon, description=api.description,
                   specialization=api.specialization, tier=api.tier, slot=api.slot)

    for fact in api.facts:
        dao.add_fact(convert_fact(fact))

    for skill in api.skills:
        dao.add_skill(skill)

    for fact in api.traited_facts:
        dao.add_traited_fact(convert_fact(fact))


def convert_attribute_bonus(api: AttributeBonusAPI) -> AttributeBonusDao:
    dao = AttributeBonusDao(attribute=api.attribute,
                            multiplier=api.multiplier, value=api.value)


def convert_stats(api: ItemStatsAPI) -> ItemStatsDao:
    dao = ItemStatsDao(id=api.id, name=api.name)

    for attribute in api.attributes:
        dao.add_attribute(convert_attribute_bonus(attribute))


def convert_item(api: ItemAPI) -> ItemDao:
    detailsDao = get_item_details(api.type, vars(api.details))
    dao = ItemDao(id=api.id, chat_link=api.chat_link, name=api.name, icon=api.icon,
                  description=api.description, type=api.type, rarity=api.rarity, details=detailsDao)
