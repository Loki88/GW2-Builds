#!/usr/bin/env python


class Fact:
    id: int
    name: str
    description: str
    icon: str
    facts: list[Fact]
    traited_facts: list[Fact]
    
    
    
    # fact requires a strategy and a hierarchy of facts to represent the different facts