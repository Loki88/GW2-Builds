#!/usr/bin/env python

from abc import ABC, abstractmethod
from model.api import Item
from model.api.api_decorator import ApiDecorator

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
        