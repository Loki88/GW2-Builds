#!/usr/bin/env python

from .utils import get_or_none, get_list_or_empty
from .enums import Attribute

class AttributeBonus:
    attribute: Attribute
    multiplier: float
    value: int
    
    def __init__(self, data : dict = None) -> None:
        if (data is not None):
            self.attribute = Attribute[get_or_none('attribute', data)]
            self.multiplier = get_or_none('multiplier', data)
            self.value = get_or_none('value', data)

class ItemStats:
    id: int
    name: str
    attributes: list[AttributeBonus]
        
    def __init__(self, data : dict = None) -> None:
        if (data is not None):
            self.id = get_or_none('id', data)
            self.name = get_or_none('name', data)

            self.attributes = [AttributeBonus(x) for x in get_list_or_empty('attributes', data)]
