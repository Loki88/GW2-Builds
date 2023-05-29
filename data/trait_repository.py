#!/usr/bin/env python

import BTrees

from model.dao import Trait
from utils import Singleton
from .db import Db


class TraitsRepository(metaclass=Singleton):

    def __init__(self) -> None:
        with Db().open_transaction() as connection:
            try:
                if connection.root.traits is not None:
                    pass
            except:
                connection.root.traits = BTrees.OOBTree.BTree()

    def save_trait(self, trait: Trait) -> Trait:
        with Db().open_transaction() as connection:
            connection.root.traits[trait.id] = trait
            return connection.root.traits[trait.id]

    def get_trait(self, id: int = None) -> list[Trait] | Trait:
        conn = None
        try:
            conn = Db().open_connection()
            if (id is None):
                return list(conn.root.traits.values())
            else:
                return conn.root.traits.get(id, None)
        finally:
            if conn is not None:
                conn.close()

    def delete_trait(self, id: int = None) -> None:
        with Db().open_transaction() as connection:
            if (id is None):
                connection.root.traits.clear()
            else:
                connection.root.traits.pop(id, None)
