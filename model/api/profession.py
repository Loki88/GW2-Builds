#!/usr/bin/env python

from typing import Callable
from .api_decorator import ApiDecorator
from .weapon import Weapon
from utils import no_duplicates


class Profession(ApiDecorator):

    def __init__(self, data: dict = None,
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = [],
                 converters: dict[str, Callable] = {}) -> None:
        super().__init__(data,
                         attributes + ['id', 'name',
                                       'code', 'icon', 'icon_big'],
                         list_attributes + ['specializations', 'flags'],
                         dict_attributes + ['weapons'],
                         {
                             'specializations': lambda x: no_duplicates([int(s) for s in x]),
                             'weapons': lambda x: [Weapon({'name': a} | b) for a, b in x.items()] if x is not None else []
                         }
                         | converters)

    def __str__(self) -> str:
        return f'Profession ({self.name}, weapons: {self.weapons})'

    def __repr__(self):
        return str(self)
