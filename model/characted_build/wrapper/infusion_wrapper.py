#!/usr/bin/env python

from model.api import Item

class InfusionWrapper(Item):

    def __init__(self, item: Item) -> None:
        self.__dict__['_item_'] = item

    def set_infusion(self, infusion: Item, slot: int):
        pass
    
    def get_infusions(self) -> Item | list[Item]:
        pass

    def __getattribute__(self, name):


        item = self.__dict__['_item_']
        

        meth = getattr(self.__class__, name, None)
        if meth is None:
            raise AttributeError(name)

        return meth.__get__(self, self.__class__)