#!/usr/bin/env python

from typing import Callable
from .api_decorator import ApiDecorator
from .utils import get_or_none, get_list_or_empty
from model.enums import Attribute


class AttributeBonus(ApiDecorator):

    def __init__(self, data: dict = None,
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = [],
                 converters: dict[str, Callable] = {}) -> None:
        super().__init__(data,
                         attributes + ['attribute', 'multiplier', 'value'],
                         list_attributes,
                         dict_attributes,
                         {
                             'attribute': lambda x: Attribute[x] if x is not None else None
                         }
                         | converters)


class ItemStats:

    def __init__(self, data: dict = None,
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = [],
                 converters: dict[str, Callable] = {}) -> None:
        super().__init__(data,
                         attributes + ['id', 'name'],
                         list_attributes + ['attributes'],
                         dict_attributes,
                         {
                             'attributes': lambda x: [AttributeBonus(a) for a in x]
                         }
                         | converters)
