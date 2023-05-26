#!/usr/bin/env python

import os
import ZODB, ZODB.FileStorage, zc.zlibstorage

from config.provider import ConfigProvider
from utils import Singleton
import BTrees

from model.dao import *

config_provider = ConfigProvider()

class Db(metaclass=Singleton):
    
    db: ZODB.DB = None
    
    def __init__(self) -> None:
        if(not os.path.exists(config_provider.get_data_dir())):
            os.makedirs(config_provider.get_data_dir())
        
        self.db = self._get_db(config_provider.get_data_file())
        self._init_collections()
        
        
    def _get_db(self, data_file: str):
        storage = ZODB.FileStorage.FileStorage(data_file)
        compressed_storage = zc.zlibstorage.ZlibStorage(storage)
        return ZODB.DB(compressed_storage)
    
    def _init_collections(self):
        with self.db.transaction() as connection:
            self._init_professions(connection)
            self._init_specializations(connection)
        
    def _init_professions(self, connection) -> None:
        try:
            if connection.root.professions is not None:
                pass
        except:
            connection.root.professions = BTrees.OOBTree.BTree()
            
    def _init_specializations(self, connection) -> None:
        try:
            if connection.root.specializations is not None:
                pass
        except:
            connection.root.specializations = BTrees.OOBTree.BTree()

    def save_build(self, build: Build) -> Build:
        with self.db.transaction() as connection:
            connection.root.build = build
            return connection.root.build

    def get_build(self) -> Build:
        conn = None
        try:
            conn = self.db.open()
            return conn.root.build
        finally:
            if conn is not None:
                conn.close()
                
    def delete_build(self) -> None:
        with self.db.transaction() as connection:
            connection.root.build = None
                
    def save_profession(self, profession: Profession) -> Profession:
        with self.db.transaction() as connection:
            connection.root.professions[profession.id] = profession
            return connection.root.professions[profession.id]
        
    def get_professions(self) -> list[Profession]:
        conn = None
        try:
            conn = self.db.open()
            return list(conn.root.professions.itervalues())
        finally:
            if conn is not None:
                conn.close()
                
    def get_profession_by_id(self, id: int) -> Profession:
        conn = None
        try:
            conn = self.db.open()
            return conn.root.professions[id]
        except KeyError:
            return None
        finally:
            if conn is not None:
                conn.close()
    
    def get_profession_by_name(self, name: str = None) -> list[Profession]:
        conn = None
        try:
            conn = self.db.open()
            return [x for x in conn.root.professions.itervalues() if x.name is name]
        finally:
            if conn is not None:
                conn.close()
                
    def delete_professions(self):
        with self.db.transaction() as connection:
            connection.root.professions.clear()
    
    def delete_profession_by_id(self, id: int):
        with self.db.transaction() as connection:
            connection.root.professions.pop(id)
    
    def save_specialization(self, specialization: Specialization):
        with self.db.transaction() as connection:
            connection.root.specializations[specialization.id] = specialization
            return connection.root.specializations[specialization.id]
        
    def get_specializations(self) -> list[Specialization]:
        conn = None
        try:
            conn = self.db.open()
            return list(conn.root.specializations.itervalues())
        finally:
            if conn is not None:
                conn.close()
                
    def get_specialization_by_id(self, id: int) -> Specialization:
        conn = None
        try:
            conn = self.db.open()
            return conn.root.specializations[id]
        except KeyError:
            return None
        finally:
            if conn is not None:
                conn.close()
    
    def get_specialization_by_name(self, name: str = None) -> list[Specialization]:
        conn = None
        try:
            conn = self.db.open()
            return [x for x in conn.root.specializations.itervalues() if x.name is name]
        finally:
            if conn is not None:
                conn.close()
                
    def delete_specializations(self):
        with self.db.transaction() as connection:
            connection.root.specializations.clear()
    
    def delete_specialization_by_id(self, id: int):
        with self.db.transaction() as connection:
            connection.root.specializations.pop(id)
    
    def __del__(self):
        self.db.close()