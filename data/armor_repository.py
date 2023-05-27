#!/usr/bin/env python

import BTrees

from model.dao import Item, ArmorDetail
from model import ItemType, ArmorWeight, ArmorType
from utils import Singleton
from .db import Db


class ArmorRepository(metaclass=Singleton):

    def __init__(self) -> None:
        with Db().open_transaction() as connection:
            try:
                if connection.root.armor is not None:
                    pass
            except:
                connection.root.armor = BTrees.OOBTree.BTree()

    def save_armor(self, armor: Item) -> Item:
        if (armor.type == ItemType.Armor):
            details: ArmorDetail = armor.details
            with Db().open_transaction() as connection:
                connection.root.armor[details.weight_class][details.type] = armor
                return connection.root.armor[details.weight_class][details.type]
        else:
            raise ValueError(armor)

    def get_armor(self) -> list[Item]:
        conn = None
        try:
            conn = Db().open_connection()
            return list(conn.root.armor.itervalues())
        finally:
            if conn is not None:
                conn.close()

    def get_armor_by_weight(self, weight: ArmorWeight) -> list[Item]:
        conn = None
        try:
            conn = Db().open_connection()
            return list(conn.root.armor[weight].itervalues())
        finally:
            if conn is not None:
                conn.close()
