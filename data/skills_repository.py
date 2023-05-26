#!/usr/bin/env python

import BTrees

from model.dao import Specialization
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
    
    
    def save_specialization(self, specialization: Specialization):
        with Db().open_transaction() as connection:
            connection.root.skills[specialization.id] = specialization
            return connection.root.skills[specialization.id]
        
    def get_specializations(self) -> list[Specialization]:
        conn = None
        try:
            conn = Db().open_connection()
            return list(conn.root.skills.itervalues())
        finally:
            if conn is not None:
                conn.close()
                
    def get_specialization_by_id(self, id: int) -> Specialization:
        conn = None
        try:
            conn = Db().open_connection()
            return conn.root.skills[id]
        except KeyError:
            return None
        finally:
            if conn is not None:
                conn.close()
    
    def get_specialization_by_name(self, name: str = None) -> list[Specialization]:
        conn = None
        try:
            conn = Db().open_connection()
            return [x for x in conn.root.skills.itervalues() if x.name is name]
        finally:
            if conn is not None:
                conn.close()
                
    def delete_specializations(self):
        with Db().open_transaction() as connection:
            connection.root.skills.clear()
    
    def delete_specialization_by_id(self, id: int):
        with Db().open_transaction() as connection:
            connection.root.skills.pop(id)
