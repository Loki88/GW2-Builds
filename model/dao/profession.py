#!/usr/bin/env python

import persistent
import persistent.list
import BTrees
from .weapon import Weapon

class Profession(persistent.Persistent):
    
    
    def __init__(self, id: int, name: str, code: int, icon: str, icon_big: str) -> None:
        super().__init__()
        self.id = id
        self.name = name
        self.code = code
        self.icon = icon
        self.icon_big = icon_big
        
        self.specializations = persistent.list.PersistentList()
        self.weapons = BTrees.OOBTree.TreeSet()
        self.flags = persistent.list.PersistentList()
        
    def add_specialization(self, specialization: int):
        if(specialization not in self.specializations):
            self.specializations.append(specialization)
            
    def _weapon_key(sekf, weapon: Weapon) -> str:
        return weapon.name + '-' + str(weapon.specialization)
            
    def add_weapon(self, weapon: Weapon):
        self.weapons.add(weapon)
        
    def add_flag(self, flag: str):
        if(flag not in self.flags):
            self.flags.append(flag)
