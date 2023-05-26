#!/usr/bin/env python

import persistent
import persistent.list

class Specialization(persistent.Persistent):
    
    def __init__(self, id: int, name: str, profession: int, elite: bool, icon: str, background: str) -> None:
        super().__init__()
        self.id = id
        self.name = name
        self.elite = elite
        self.profession = profession
        self.icon = icon
        self.background = background
        
        self.minor_traits = persistent.list.PersistentList()
        self.major_traits = persistent.list.PersistentList()
        
    def add_minor_trait(self, trait: int):
        if(trait not in self.minor_traits):
            self.minor_traits.append(trait)
        
    def add_major_trait(self, trait: int):
        if(trait not in self.major_traits):
            self.major_traits.append(trait)
