#!/usr/bin/env python

import persistent
import persistent.list
import BTrees
from .fact import Fact

class Trait(persistent.Persistent):
    
    def __init__(self, id: int, name: str, icon: str, description: str, specialization: int, tier: int, slot: str) -> None:
        super().__init__()
        self.id = id
        self.name = name
        self.icon = icon
        self.description = description
        self.specialization = specialization
        self.tier = tier
        self.slot = slot
        
        self.facts = BTrees.OOBTree.TreeSet()
        self.traited_facts = BTrees.OOBTree.TreeSet()
        self.skills = persistent.list.PersistentList()
        
    def add_fact(self, fact: Fact):
        self.facts.add(fact)
        
    def add_traited_fact(self, fact: Fact):
        self.traited_facts.add(fact)
        
    def add_skill(self, skill: int):
        if(skill not in self.skills):
            self.skills.append(skill)