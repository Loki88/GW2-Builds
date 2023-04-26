#!/usr/bin/env python

from weapon import Weapon


class Profession:
    id: str
    name: str
    code: int
    icon: str
    icon_big: str
    specialization: list[int]
    weapons: list[Weapon]
    flags: list[str]


    def __init__(self, data : dict = None) -> None:
        if (data is not None):
            self.id = data['id']
            self.name = data['name']
            self.code = data['code']
            self.icon = data['icon']
            self.icon_big = data['icon_big']

            if(data['specialization'] is not None):
                self.specialization = [int(x) for x in data['specialization']]

            if(data['weapons'] is not None):
                self.weapons = [Weapon(x) for x in data['weapons']]

            self.flags = data['flags']
