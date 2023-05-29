#!/usr/bin/env python

import BTrees

from model.dao import Item, WeaponDetail
from model import ItemType, WeaponType
from utils import Singleton
from .db import Db


class WeaponsRepository(metaclass=Singleton):

    def __init__(self) -> None:
        with Db().open_transaction() as connection:
            try:
                if connection.root.weapons is not None:
                    pass
            except:
                connection.root.weapons = BTrees.OOBTree.BTree()

    def save_weapon(self, weapon: Item):
        if (weapon.type == ItemType.Weapon):
            details: WeaponDetail = weapon.details
            with Db().open_transaction() as connection:
                connection.root.weapons[details.type.value] = weapon
                return connection.root.weapons[details.type.value]
        else:
            raise ValueError(weapon)

    def get_weapon(self, type: WeaponType = None) -> list[Item] | Item:
        conn = None
        try:
            conn = Db().open_connection()
            if (type is None):
                return list(conn.root.weapons.values())
            else:
                return conn.root.weapons.get(type.value, None)
        finally:
            if conn is not None:
                conn.close()

    def delete_weapon(self, type: WeaponType = None) -> None:
        with Db().open_transaction() as connection:
            if (type is None):
                connection.root.weapons.clear()
            else:
                connection.root.weapons.pop(type.value, None)
