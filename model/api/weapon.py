#!/usr/bin/env python

from .utils import *


class WeaponSkill:
    id: int
    slot: str

    def __init__(self, data: dict[str] = None) -> None:
        self.id = int(get_or_none('id', data))
        self.slot = get_or_none('slot', data)


class Weapon:
    name: str
    specialization: int  # Weapons supported by all specializatiions will have None
    skills: list[WeaponSkill]

    def __init__(self, name: str, data: dict[str] = None) -> None:
        self.name = name
        self.specialization = get_or_none('specialization', data)
        self.skills = [WeaponSkill(x)
                       for x in get_list_or_empty('skills', data)]

    def __str__(self) -> str:
        return f'Weapon ({self.name}, spec: {self.specialization})'

    def __repr__(self):
        return str(self)
