#!/usr/bin/env python

from .utils import *
from .specialization import Specialization
from .fact import get_fact, Fact
from .skill import Skill


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
            self.id = get_or_none('id', data)
            self.name = get_or_none('name', data)
            self.icon = get_or_none('icon', data)
            self.description = get_or_none('description', data)
            self.specialization = get_or_none('specialization', data)
            self.tier = get_or_none('tier', data)
            self.facts = [get_fact(x) for x in get_list_or_empty('facts', data)]
            self.traited_facts = [get_fact(x) for x in get_list_or_empty('traited_facts', data)]
            self.skills = [Skill(x) for x in get_list_or_empty('skills', data)]
