#!/usr/bin/env python

from .utils import *
from .fact import get_fact, Fact

class Skill:
    id: int
    name: str
    description: str
    icon: str
    facts: list[Fact]
    traited_facts: list[Fact]
    
    def __init__(self, data: dict = None) -> None:
        if(data is not None):
            self.id = get_or_none('id', data)
            self.name = get_or_none('name', data)
            self.description = get_or_none('description', data)
            self.icon = get_or_none('icon', data)
            self.facts = [get_fact(x) for x in get_list_or_empty('facts', data)]
            self.traited_facts = [get_fact(x) for x in get_list_or_empty('traited_facts', data)]
    