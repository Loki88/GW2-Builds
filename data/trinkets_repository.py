#!/usr/bin/env python

import persistent

from model import Item, TrinketDetail
from utils import Singleton
from .db import Db
from model import ItemType, TrinketType


class TrinketsRepository(metaclass=Singleton):

    def __init__(self) -> None:
        with Db().open_transaction() as connection:
            try:
                if connection.root.trinkets is not None:
                    pass
            except:
                connection.root.trinkets = persistent.mapping.PersistentMapping()

    def save_trinket(self, trinket: Item) -> Item:
        if (trinket.type == ItemType.Trinket):
            details: TrinketDetail = trinket.details
            with Db().open_transaction() as connection:
                connection.root.trinkets[details.type.value] = trinket
                return connection.root.trinkets[details.type.value]
        else:
            raise ValueError(trinket)

    def get_trinket(self, type: TrinketType = None) -> list[Item] | Item:
        conn = None
        try:
            conn = Db().open_connection()
            if (type is None):
                return list(conn.root.trinkets.values())
            else:
                return conn.root.trinkets.get(type.value, None)
        finally:
            if conn is not None:
                conn.close()

    def delete_trinket(self, type: TrinketType = None) -> None:
        with Db().open_transaction() as connection:
            if (type is None):
                connection.root.trinkets.clear()
            else:
                connection.root.trinkets.pop(type.value, None)
