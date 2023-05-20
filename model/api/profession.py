#!/usr/bin/env python

from .utils import *
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
            self.id = get_or_none('id', data)
            self.name = get_or_none('name', data)
            self.code = get_or_none('code', data)
            self.icon = get_or_none('icon', data)
            self.icon_big = get_or_none('icon_big', data)

            self.specializations = [int(x) for x in get_list_or_empty('specializations', data)]
            self.weapons = [Weapon(x, y) for x, y in get_dict_or_empty('weapons', data).items()]

            self.flags = data['flags']

    def __str__(self) -> str:
        return f'Profession ({self.name}, weapons: {self.weapons})'
    
    def __repr__(self):
        return str(self)