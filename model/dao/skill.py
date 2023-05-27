#!/usr/bin/env python

import persistent
import persistent.list
import BTrees
from model import SkillType, Slot, SkillCategory, SkillFlag
from .fact import Fact


class Skill(persistent.Persistent):

    def __init__(self, id: int, name: str, description: str, icon: str, chat_link: str,
                 type: SkillType = None, weapon_type: str = None, slot: Slot = None, attunement: str = None, cost: float = None,
                 dual_wield: str = None, flip_skill: int = None, initiative: float = None, next_chain: int = None,
                 prev_chain: int = None) -> None:
        super().__init__()

        self.id = id
        self.name = name
        self.description = description
        self.icon = icon
        self.chat_link = chat_link
        self.type = type
        self.weapon_type = weapon_type
        self.slot = slot
        self.attunement = attunement
        self.cost = cost
        self.dual_wield = dual_wield
        self.flip_skill = flip_skill
        self.initiative = initiative
        self.next_chain = next_chain
        self.prev_chain = prev_chain

        self.facts = BTrees.OOBTree.TreeSet()
        self.traited_facts = BTrees.OOBTree.TreeSet()
        self.professions = persistent.list.PersistentList()
        self.categories = persistent.list.PersistentList()
        self.transform_skills = persistent.list.PersistentList()
        self.bundle_skills = persistent.list.PersistentList()
        self.toolbelt_skill = persistent.list.PersistentList()
        self.flags = persistent.list.PersistentList()

    def add_fact(self, fact: Fact):
        self.facts.add(fact)

    def add_traited_fact(self, fact: Fact):
        self.traited_facts.add(fact)

    def add_profession(self, id: int):
        if (id not in self.professions):
            self.professions.append(id)

    def add_category(self, category: SkillCategory):
        if (category not in self.categories):
            self.categories.append(category)

    def add_flag(self, flag: SkillFlag):
        if (flag not in self.flags):
            self.flags.append(flag)

    def add_transform_skill(self, id: int):
        if (id not in self.transform_skills):
            self.transform_skills.append(id)

    def add_boundle_skill(self, id: int):
        if (id not in self.bundle_skills):
            self.bundle_skills.append(id)

    def add_toolbelt_skill(self, id: int):
        if (id not in self.toolbelt_skill):
            self.toolbelt_skill.append(id)
