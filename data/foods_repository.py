#!/usr/bin/env python

import BTrees

from model import Item, ConsumableDetail
from model import ItemType, ConsumableType
from utils import Singleton
from .db import Db


class FoodsRepository(metaclass=Singleton):

    def __init__(self) -> None:
        with Db().open_transaction() as connection:
            try:
                if connection.root.foods is not None:
                    pass
            except BaseException:
                connection.root.foods = BTrees.OOBTree.BTree()

    def _save_single(self, connection, food: Item):
        if (food.type == ItemType.Consumable):
            details: ConsumableDetail = food.details
            if (details.type == ConsumableType.Food):
                connection.root.foods[food.id] = food
            return
        raise ValueError(food)

    def save_food(self, food: Item | list[Item]):
        with Db().open_transaction() as connection:
            if (isinstance(food, list)):
                for x in food:
                    self._save_single(connection, x)
            else:
                self._save_single(connection, food)

    def get_food(self, id: int = None) -> list[Item] | Item:
        conn = Db().get_connection()
        if (id is None):
            return list(conn.root.foods.values())
        else:
            return conn.root.foods.get(id, None)

    def delete_food(self, id: int = None) -> None:
        with Db().open_transaction() as connection:
            if (id is None):
                connection.root.foods.clear()
            else:
                connection.root.foods.pop(id, None)
