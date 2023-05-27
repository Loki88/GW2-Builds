#!/usr/bin/env python

import BTrees

from model.dao import ItemStats
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
