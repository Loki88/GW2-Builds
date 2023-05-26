#!/usr/bin/env python

import BTrees

from model.dao import ItemStats
from utils import Singleton
from .db import Db

class ArmorRepository(metaclass=Singleton):
        
    def __init__(self) -> None:
        with Db().open_transaction() as connection:
            try:
                if connection.root.armor is not None:
                    pass
            except:
                connection.root.stats = BTrees.OOBTree.BTree()                
    
    
   