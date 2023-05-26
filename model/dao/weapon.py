#!/usr/bin/env python

import persistent
import persistent.list
from BTrees.OOBTree import TreeSet

    
class WeaponSkill(persistent.Persistent):
    
    def __init__(self, id: int, slot: str) -> None:
        self.id = id
        self.slot = slot
        
    def __eq__(self, other) -> bool:
        if other.__class__ is WeaponSkill:
            return self.id == other.id and self.slot == other.slot
        else:
            return False


class Weapon(persistent.Persistent):
    name: str
    specialization: int
    skills: list[WeaponSkill]

    def __init__(self, name: str, specialization: int) -> None:
        self.name = name
        self.specialization = specialization
        self.skills = TreeSet()

    def add_skill(self, skill: WeaponSkill):
        self.skills.append(skill)

    def __eq__(self, other) -> bool:
        if other.__class__ is Weapon:
            return self.name is other.name and self.specialization == other.specialization and self.skills == other.skills
        else:
            return False
        
    def __lt__(self, other) -> bool:
        return self.name.__lt__(other.name)