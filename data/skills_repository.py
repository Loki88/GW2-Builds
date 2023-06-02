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

    def save_skill(self, skill: Skill | list[Skill]):
        with Db().open_transaction() as connection:
            if (isinstance(skill, list)):
                for x in skill:
                    self._save_single(connection, x)
            else:
                self._save_single(connection, skill)

    def get_skills(self, id: int = None, name: str = None) -> list[Skill]:
        conn = Db().get_connection()
        if (id is None and name is None):
            return list(conn.root.skills.itervalues())
        elif (id is None):
            return [x for x in conn.root.skills.itervalues() if x.name == name]
        elif (name is None):
            return conn.root.skills.get(id, None)
        else:
            skill = conn.root.skills.get(id, None)
            return skill if skill is not None and skill.name == name else None

    def delete_skills(self, id: int = None):
        with Db().open_transaction() as connection:
            if (id is None):
                connection.root.skills.clear()
            else:
                connection.root.skills.pop(id)
