#!/usr/bin/env python

import persistent
from typing import Callable
from abc import ABC
from .utils import get_or_none, get_list_or_empty, get_dict_or_empty
from persistent.tests.attrhooks import VeryPrivate


class ApiDecorator(persistent.Persistent, ABC):

    def __init__(self, data: dict,
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = [],
                 converters: dict[str, Callable] = {}):
        super().__init__()
        self.__dict__['_data_'] = {}
        self.__dict__['_expected_attributes_'] = attributes
        self.__dict__['_expected_list_attributes_'] = list_attributes
        self.__dict__['_expected_dict_attributes_'] = dict_attributes
        if (data is not None):
            self._prepare_data(data, converters)

    def _prepare_data(self, data: dict,
                      converters: dict[str, Callable] = {}
                      ) -> dict:
        for attr in self.__dict__['_expected_attributes_']:
            self.__dict__['_data_'][attr] = self._prepare_single(
                attr, data, converters, get_or_none)

        for attr in self.__dict__['_expected_list_attributes_']:
            self.__dict__['_data_'][attr] = self._prepare_single(
                attr, data, converters, get_list_or_empty)

        for attr in self.__dict__['_expected_dict_attributes_']:
            self.__dict__['_data_'][attr] = self._prepare_single(
                attr, data, converters, get_dict_or_empty)

    def _prepare_single(self,
                        attr: str,
                        data: dict,
                        converters: dict[str,
                                         Callable],
                        get_value: Callable[[str],
                                            dict]) -> object:
        value = get_value(attr, data)
        if (attr in converters):
            value = converters[attr](value)
        return value

    def __getattribute__(self, name):
        if persistent.Persistent._p_getattr(self, name):
            return persistent.Persistent.__getattribute__(self, name)

        data = self.__dict__['_data_']
        expected_attributes = self.__dict__['_expected_attributes_']
        if name in expected_attributes:
            return get_or_none(name, data)

        expected_list_attributes = self.__dict__['_expected_list_attributes_']
        if name in expected_list_attributes:
            return get_list_or_empty(name, data)

        expected_dict_attributes = self.__dict__['_expected_dict_attributes_']
        if name in expected_dict_attributes:
            return get_dict_or_empty(name, data)

        meth = getattr(self.__class__, name, None)
        if meth is None:
            raise AttributeError(name)

        return meth.__get__(self, self.__class__)

    def __setattr__(self, name, value):
        if persistent.Persistent._p_setattr(self, name, value):
            return

        self.__dict__['_data_'][name] = value

        if not name.startswith('tmp_'):
            self._p_changed = 1

    def __delattr__(self, name):
        if persistent.Persistent._p_delattr(self, name):
            return

        del self.__dict__['_data_'][name]

        if not name.startswith('tmp_'):
            self._p_changed = 1
