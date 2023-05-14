#!/usr/bin/env python

from .weapon import Weapon


class Profession:
    id: str
    name: str
    code: int
    icon: str
    icon_big: str
    specializations: list[int]
    weapons: list[Weapon]
    flags: list[str]


    def __init__(self, data : dict = None) -> None:
        if (data is not None):
            self.id = data['id']
            self.name = data['name']
            self.code = data['code'] if 'code' in data else None
            self.icon = data['icon'] if 'icon' in data else None
            self.icon_big = data['icon_big'] if 'icon_big' in data else None

            self.specializations = [int(x) for x in data['specializations']]
            self.weapons = [Weapon(x, y) for x, y in data['weapons'].items()]

            self.flags = data['flags']

    def __str__(self) -> str:
        return f'Profession ({self.name}, weapons: {self.weapons})'
    
    def __repr__(self):
        return str(self)