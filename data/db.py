#!/usr/bin/env python

import os
import ZODB, ZODB.FileStorage, zc.zlibstorage
from config.provider import ConfigProvider
from utils import Singleton

config_provider = ConfigProvider()

class Db(metaclass=Singleton):
    
    db: ZODB.DB
    
    def __init__(self) -> None:
        if(not os.path.exists(config_provider.get_data_dir())):
            os.makedirs(config_provider.get_data_dir())
        
        storage = ZODB.FileStorage.FileStorage(config_provider.get_data_file())
        compressed_storage = zc.zlibstorage.ZlibStorage(storage)
        self.db = ZODB.DB(compressed_storage)

