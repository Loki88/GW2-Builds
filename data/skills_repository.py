#!/usr/bin/env python

import BTrees

from model import Skill
from utils import Singleton
from .db import Db


class SkillsRepository(metaclass=Singleton):

    def __init__(self) -> None:
        with Db().open_transaction() as connection:
            try:
                if connection.root.skills is not None:
                    pass
            except:
                connection.root.skills = BTrees.OOBTree.BTree()

    def _save_single(self, connection, skill: Skill):
        connection.root.skills[skill.id] = skill
        return connection.root.skills[skill.id]

    def save_skill(self, skill: Skill | list[Skill]) -> Skill | list[Skill]:
        with Db().open_transaction() as connection:
            if (isinstance(skill, list)):
                return [self._save_single(x) for x in skill]
            else:
                return self._save_single(skill)

    def get_skills(self) -> list[Skill]:
        conn = None
        try:
            conn = Db().open_connection()
            return list(conn.root.skills.itervalues())
        finally:
            if conn is not None:
                conn.close()

    def get_skill_by_id(self, id: int) -> Skill:
        conn = None
        try:
            conn = Db().open_connection()
            return conn.root.skills[id]
        except KeyError:
            return None
        finally:
            if conn is not None:
                conn.close()

    def get_skill_by_name(self, name: str = None) -> list[Skill]:
        conn = None
        try:
            conn = Db().open_connection()
            return [x for x in conn.root.skills.itervalues() if x.name is name]
        finally:
            if conn is not None:
                conn.close()

    def delete_skills(self):
        with Db().open_transaction() as connection:
            connection.root.skills.clear()

    def delete_skill_by_id(self, id: int):
        with Db().open_transaction() as connection:
            connection.root.skills.pop(id)
