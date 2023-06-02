#!/usr/bin/env python

from typing import Callable
from .api_decorator import ApiDecorator


class Specialization(ApiDecorator):

    def __init__(self, data: dict = None,
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = [],
                 converters: dict[str, Callable] = {}) -> None:
        super().__init__(data,
                         attributes + ['id', 'name', 'profession',
                                       'elite', 'icon', 'background'],
                         list_attributes + ['minor_traits', 'major_traits'],
                         dict_attributes,
                         {
                             'minor_traits': lambda x: [int(t) for t in x],
                             'major_traits': lambda x: [int(t) for t in x],
                         }
                         | converters)
