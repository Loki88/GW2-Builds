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

    def _save_single(self, connection, trinket: Item):
        if (trinket.type == ItemType.Trinket):
            details: TrinketDetail = trinket.details
            connection.root.trinkets[details.type.value] = trinket
        else:
            raise ValueError(trinket)

    def save_trinket(self, trinket: Item | list[Item]):
        with Db().open_transaction() as connection:
            if (isinstance(trinket, list)):
                for x in trinket:
                    self._save_single(connection, x)
            else:
                self._save_single(connection, trinket)

    def get_trinket(self, type: TrinketType = None) -> list[Item] | Item:
        conn = Db().get_connection()
        if (type is None):
            return list(conn.root.trinkets.values())
        else:
            return conn.root.trinkets.get(type.value, None)

    def delete_trinket(self, type: TrinketType = None) -> None:
        with Db().open_transaction() as connection:
            if (type is None):
                connection.root.trinkets.clear()
            else:
                connection.root.trinkets.pop(type.value, None)
