#!/usr/bin/env python

from typing import Callable
from .api_decorator import ApiDecorator
from .fact import get_fact
from .skill import Skill


class Trait(ApiDecorator):

    def __init__(self, data: dict = None,
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = [],
                 converters: dict[str, Callable] = {}) -> None:
        super().__init__(data,
                         attributes + ['id', 'name', 'icon',
                                       'description', 'specialization', 'tier'],
                         list_attributes +
                         ['facts', 'traited_facts', 'skills'],
                         dict_attributes,
                         {
                             'facts': lambda x: [get_fact(f) for f in x],
                             'traited_facts': lambda x: [get_fact(f) for f in x],
                             'skills': lambda x: [Skill(s) for s in x],
                         }
                         | converters)
