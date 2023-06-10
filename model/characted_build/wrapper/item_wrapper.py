#!/usr/bin/env python

from abc import ABC, abstractmethod
from model.api import Item
from model.enums import UpgradeComponentType

class ItemWrapper(Item, ABC):

    def __init__(self, item: Item, 
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = []) -> None:
        self.__dict__['_data_'] = {}
        self.__dict__['_expected_attributes_'] = ['item'] + attributes
        self.__dict__['_expected_list_attributes_'] = list_attributes
        self.__dict__['_expected_dict_attributes_'] = dict_attributes
        self.item = item

    def __getattribute__(self, name):
        try:
            return super().__getattribute__(name)
        except AttributeError:
            return self.item.__getattribute__(name)

    @abstractmethod
    def _held_component(self) -> UpgradeComponentType:
        pass

    def can_hold(self, upgrade: UpgradeComponentType) -> bool:
        if(upgrade == self._held_component()):
            return True
        else:
            try:
                return self.item.can_hold(upgrade)
            except:
                return False

    @abstractmethod
    def upgrade(self, upgrade: Item | list[Item], slot: int = None):
        pass