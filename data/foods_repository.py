#!/usr/bin/env python

import BTrees

from model.dao import Item, ConsumableDetail
from model import ItemType, ConsumableType
from utils import Singleton
from .db import Db


class FoodsRepository(metaclass=Singleton):

    def __init__(self) -> None:
        with Db().open_transaction() as connection:
            try:
                if connection.root.foods is not None:
                    pass
            except:
                connection.root.foods = BTrees.OOBTree.BTree()

    def save_food(self, food: Item) -> Item:
        if (food.type == ItemType.Consumable):
            details: ConsumableDetail = food.details
            if (details.type == ConsumableType.Food):
                with Db().open_transaction() as connection:
                    connection.root.foods[food.id] = food
                    return connection.root.foods[food.id]
        raise ValueError(food)

    def get_food(self, id: int = None) -> list[Item] | Item:
        conn = None
        try:
            conn = Db().open_connection()
            if (id is None):
                return list(conn.root.foods.values())
            else:
                return conn.root.foods.get(id, None)
        finally:
            if conn is not None:
                conn.close()

    def delete_food(self, id: int = None) -> None:
        with Db().open_transaction() as connection:
            if (id is None):
                connection.root.foods.clear()
            else:
                connection.root.foods.pop(id, None)
