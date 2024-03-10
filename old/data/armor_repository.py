#!/usr/bin/env python

import BTrees
import persistent

from model import Item, ArmorDetail, ItemType, ArmorWeight, ArmorType
from utils import Singleton, flatten
from .db import Db


class ArmorRepository(metaclass=Singleton):

    def __init__(self) -> None:
        with Db().open_transaction() as connection:
            try:
                if connection.root.armor is not None:
                    pass
            except BaseException:
                connection.root.armor = persistent.mapping.PersistentMapping()

    def _save_single(self, connection, armor: Item):
        if (armor.type == ItemType.Armor):
            details: ArmorDetail = armor.details
            if (details.weight_class.value not in connection.root.armor):
                connection.root.armor[details.weight_class.value] = persistent.mapping.PersistentMapping(
                )
            connection.root.armor[details.weight_class.value][details.type.value] = armor
        else:
            raise ValueError(armor)

    def save_armor(self, armor: Item | list[Item]):
        with Db().open_transaction() as connection:
            if (isinstance(armor, list)):
                for x in armor:
                    self._save_single(connection, x)
            else:
                self._save_single(connection, armor)

    def _get_armors(self, conn) -> list[Item]:
        return flatten([x.values() for x in conn.root.armor.values()])

    def get_armor(self, weight: ArmorWeight = None, type: ArmorType = None) -> list[Item] | Item:
        conn = Db().get_connection()
        if (type is None and weight is None):
            return self._get_armors(conn)
        elif (type is None):
            if (weight.value in conn.root.armor):
                return list(conn.root.armor[weight.value].values())
            else:
                return []
        elif (weight is None):
            return [x[type.value] for x in conn.root.armor.values() if type.value in x]
        else:
            weight_map = conn.root.armor.get(weight.value, None)
            return weight_map.get(type.value, None) if weight_map is not None else None

    def delete_armor(self, weight: ArmorWeight = None, type: ArmorType = None) -> None:
        with Db().open_transaction() as connection:
            if (type is None and weight is None):
                connection.root.armor.clear()
            elif (type is None):
                connection.root.armor.pop(weight.value, None)
            elif (weight is None):
                for x in connection.root.armor.values():
                    x.pop(type.value, None)
            else:
                if (weight.value in connection.root.armor):
                    connection.root.armor[weight.value].pop(type.value, None)
