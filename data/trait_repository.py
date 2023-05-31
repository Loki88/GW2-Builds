#!/usr/bin/env python

import BTrees

from model import Trait
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

    def _save_single(self, connection, trait: Trait) -> Trait:
        connection.root.traits[trait.id] = trait
        return connection.root.traits[trait.id]

    def save_trait(self, trait: Trait | list[Trait]) -> Trait | list[Trait]:
        with Db().open_transaction() as connection:
            if (isinstance(trait, list)):
                return [self._save_single(connection, x) for x in trait]
            else:
                return self._save_single(connection, trait)

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
