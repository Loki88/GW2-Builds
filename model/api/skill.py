#!/usr/bin/env python

from typing import Callable
from .api_decorator import ApiDecorator
from .fact import get_fact
from model.enums import SkillType, Slot, SkillCategory, SkillFlag


class Skill(ApiDecorator):

    def __init__(self, data: dict = None,
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = [],
                 converters: dict[str, Callable] = {}) -> None:
        super().__init__(data,
                         attributes + ['id', 'name', 'description', 'icon', 'chat_link', 'type',
                                       'weapon_type', 'slot', 'attunement', 'cost', 'dual_wield',
                                       'flip_skill', 'initiative', 'next_chain', 'prev_chain', 'toolbelt_skill'],
                         list_attributes + ['facts', 'traited_facts', 'professions', 'categories',
                                            'transform_skills', 'bundle_skills', 'flags'],
                         dict_attributes,
                         {
                             'type': lambda x: SkillType[x] if x is not None else None,
                             'slot': lambda x: Slot[x] if x is not None else None,
                             'facts': lambda x: [get_fact(f) for f in x],
                             'traited_facts': lambda x: [get_fact(f) for f in x],
                             'categories': lambda x: [self._get_category(c) for c in x],
                             'transform_skills': lambda x: [int(s) for s in x],
                             'bundle_skills': lambda x: [int(s) for s in x],
                             'flags': lambda x: [SkillFlag[f] for f in x],
                         }
                         | converters)

    def _get_category(self, value: str) -> SkillCategory:
        if value in SkillCategory._member_names_:
            return SkillCategory[value]
        else:
            return SkillCategory.Others
