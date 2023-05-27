#!/usr/bin/env python

import BTrees

from model.dao import Profession
from utils import Singleton
from .db import Db


class ProfessionsRepository(metaclass=Singleton):

    def __init__(self) -> None:
        with Db().open_transaction() as connection:
            try:
                if connection.root.professions is not None:
                    pass
                else:
                    connection.root.professions = BTrees.OOBTree.BTree()
            except:
                connection.root.professions = BTrees.OOBTree.BTree()

    def save_profession(self, profession: Profession) -> Profession:
        with Db().open_transaction() as connection:
            connection.root.professions[profession.id] = profession
            return connection.root.professions[profession.id]

    def get_professions(self) -> list[Profession]:
        conn = None
        try:
            conn = Db().open_connection()
            return list(conn.root.professions.itervalues())
        finally:
            if conn is not None:
                conn.close()

    def get_profession_by_id(self, id: int) -> Profession:
        conn = None
        try:
            conn = Db().open_connection()
            return conn.root.professions[id]
        except KeyError:
            return None
        finally:
            if conn is not None:
                conn.close()

    def get_profession_by_name(self, name: str = None) -> list[Profession]:
        conn = None
        try:
            conn = Db().open_connection()
            return [x for x in conn.root.professions.itervalues() if x.name is name]
        finally:
            if conn is not None:
                conn.close()

    def delete_professions(self):
        with Db().open_transaction() as connection:
            connection.root.professions.clear()

    def delete_profession_by_id(self, id: int):
        with Db().open_transaction() as connection:
            connection.root.professions.pop(id)
