#!/usr/bin/env python

import BTrees

from model.dao import ItemStats
from utils import Singleton
from .db import Db


class RunesRepository(metaclass=Singleton):

    def __init__(self) -> None:
        with Db().open_transaction() as connection:
            try:
                if connection.root.runes is not None:
                    pass
            except:
                connection.root.runes = BTrees.OOBTree.BTree()
