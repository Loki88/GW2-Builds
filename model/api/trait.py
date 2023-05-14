#!/usr/bin/env python
from model.api.specialization import Specialization



class Trait:
    
    id: int
    name: str
    icon: str
    description: str
    specialization: int
    tier: int
    slot: str
    facts: list[Fact]
    traited_facts: list[Fact]
    skills: list[Skill]

    def __init__(self, data: dict = None) -> None:
        if(data is not None):
            self.id = data['id']
            self.name = data['name']
            self.specialization = data['specialization']
            self.specialization = data['specialization']
            self.icon = data['icon']
            self.tier = data['tier']
            self.facts = [Fact(x) for x in data['facts']]
            self.traited_facts = [Fact(x) for x in data['traited_facts']]
        
