#!/usr/bin/env python

import persistent
import persistent.list
from model import Attribute


class AttributeBonus(persistent.Persistent):
    attribute: Attribute
    multiplier: float
    value: int

    def __init__(self, attribute: Attribute, multiplier: float, value: int) -> None:
        super().__init__()
        self.attribute = attribute
        self.multiplier = multiplier
        self.value = value


class ItemStats(persistent.Persistent):
    id: int
    name: str
    attributes: list[AttributeBonus]

    def __init__(self, id: int, name: str) -> None:
        super().__init__()
        self.id = id
        self.name = name

        self.attributes = persistent.list.PersistentList()

    def add_attribute(self, attribute: AttributeBonus):
        self.attributes.append(attribute)
