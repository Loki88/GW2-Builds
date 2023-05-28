#!/usr/bin/env python

import BTrees
import persistent

from model.dao import Item, ArmorDetail
from model import ItemType, ArmorWeight, ArmorType
from utils import Singleton, flatten
from .db import Db


class ArmorRepository(metaclass=Singleton):

    def __init__(self) -> None:
        with Db().open_transaction() as connection:
            try:
                if connection.root.armor is not None:
                    pass
            except:
                connection.root.armor = persistent.mapping.PersistentMapping()

    def save_armor(self, armor: Item) -> Item:
        if (armor.type == ItemType.Armor):
            details: ArmorDetail = armor.details
            with Db().open_transaction() as connection:
                if (details.weight_class.value not in connection.root.armor):
                    connection.root.armor[details.weight_class.value] = persistent.mapping.PersistentMapping(
                    )
                connection.root.armor[details.weight_class.value][details.type.value] = armor
                return connection.root.armor[details.weight_class.value][details.type.value]
        else:
            raise ValueError(armor)

    def _get_armors(self, conn) -> list[Item]:
        return flatten([x.values() for x in conn.root.armor.values()])

    def get_armor(self, weight: ArmorWeight = None, type: ArmorType = None) -> list[Item] | Item:
        conn = None
        try:
            conn = Db().open_connection()
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
                if (weight.value in conn.root.armor):
                    if (type.value in conn.root.armor[weight.value]):
                        return conn.root.armor[weight.value][type.value]
                return None

        finally:
            if conn is not None:
                conn.close()

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
