#!/usr/bin/env python

from model.api import Item
from model.characted_build.wrapper import InfusionWrapper, RuneWrapper, SigilWrapper
from utils import Singleton


class BuildFactory(metaclass=Singleton):
    # this class has to provide items and decorate them to support upgrades

    def wrap_item(self, item: Item) -> Item:
        wrapped_item = item
        if (InfusionWrapper.supports(item)):
            wrapped_item = InfusionWrapper(item)
        if (RuneWrapper.supports(item)):
            wrapped_item = RuneWrapper(wrapped_item)
        if (SigilWrapper.supports(item)):
            wrapped_item = SigilWrapper(wrapped_item)
        return wrapped_item
