#!/usr/bin/env python

from .utils import *
from .fact import get_fact, Fact
from .enums import SkillType, Slot, SkillCategory, SkillFlag


class Skill:
    id: int
    name: str
    description: str
    icon: str
    chat_link: str
    type: SkillType | None
    weapon_type: str | None
    facts: list[Fact]
    traited_facts: list[Fact]
    professions: list[str]
    slot: Slot | None
    categories: list[SkillCategory]
    attunement: str | None
    cost: float | None
    dual_wield: str | None
    flip_skill: int | None
    initiative: float | None
    next_chain: int | None
    prev_chain: int | None
    transform_skills: list[int]
    bundle_skills: list[int]
    toolbelt_skill: list[int]
    flags: list[SkillFlag]

    def __init__(self, data: dict = None) -> None:
        if (data is not None):
            self.id = get_or_none('id', data)
            self.name = get_or_none('name', data)
            self.description = get_or_none('description', data)
            self.icon = get_or_none('icon', data)
            self.chat_link = get_or_none('chat_link', data)
            self.type = self._get_skill_type(get_or_none('type', data))
            self.weapon_type = get_or_none('weapon_type', data)
            self.facts = [get_fact(x)
                          for x in get_list_or_empty('facts', data)]
            self.traited_facts = [
                get_fact(x) for x in get_list_or_empty('traited_facts', data)]
            self.professions = get_list_or_empty('professions', data)
            self.slot = self._get_slot(get_or_none('slot', data))
            self.categories = [self._get_category(
                x) for x in get_list_or_empty('categories')]
            self.attunement = get_or_none('attunement', data)
            self.cost = get_or_none('cost', data)
            self.dual_wield = get_or_none('dual_wield', data)
            self.flip_skill = get_or_none('flip_skill', data)
            self.initiative = get_or_none('initiative', data)
            self.next_chain = get_or_none('next_chain', data)
            self.prev_chain = get_or_none('prev_chain', data)
            self.transform_skills = [
                int(x) for x in get_list_or_empty('transform_skills', data)]
            self.bundle_skills = [
                int(x) for x in get_list_or_empty('bundle_skills', data)]
            self.toolbelt_skill = [
                int(x) for x in get_list_or_empty('toolbelt_skill', data)]
            self.flags = [SkillFlag[x]
                          for x in get_list_or_empty('flags', data)]

    def _get_skill_type(self, value: str | None):
        if (value is not None):
            return SkillType[value]
        return None

    def _get_slot(self, value: str | None):
        if (value is not None):
            return Slot[value]
        return None

    def _get_category(self, value: str) -> SkillCategory:
        if value in SkillCategory._member_names_:
            return SkillCategory[value]
        else:
            return SkillCategory.Others
