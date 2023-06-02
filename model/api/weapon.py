#!/usr/bin/env python

from typing import Callable
from .api_decorator import ApiDecorator


class WeaponSkill(ApiDecorator):

    def __init__(self, data: dict = None,
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = [],
                 converters: dict[str, Callable] = {}) -> None:
        super().__init__(data,
                         attributes + ['id', 'slot'],
                         list_attributes,
                         dict_attributes,
                         converters)


class Weapon(ApiDecorator):
    name: str
    specialization: int  # Weapons supported by all specializatiions will have None
    skills: list[WeaponSkill]

    def __init__(self, data: dict = None,
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = [],
                 converters: dict[str, Callable] = {}) -> None:
        super().__init__(data,
                         attributes + ['name', 'specialization'],
                         list_attributes + ['skills'],
                         dict_attributes,
                         {
                             'skills': lambda x: [WeaponSkill(s) for s in x]
                         }
                         | converters)

    def __str__(self) -> str:
        return f'Weapon ({self.name}, spec: {self.specialization})'

    def __repr__(self):
        return str(self)
