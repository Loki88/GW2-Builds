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
        
    def _get_db(self, data_file: str):
        storage = ZODB.FileStorage.FileStorage(data_file)
        compressed_storage = zc.zlibstorage.ZlibStorage(storage)
        return ZODB.DB(compressed_storage)
            
    def open_transaction(self):
        return self.db.transaction()
    
    def open_connection(self):
        return self.db.open()
    
    def __del__(self):
        self.db.close()
