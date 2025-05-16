# -*- coding: utf-8 -*-
from typing import Union, Dict

class BlockType(object):
    """
    The type (or template) of a block. 
    Does not contain permutation data (state) other than the type of block it represents.
    """

    def __init__(self, id):
        # type: (str) -> None
        self.__id = id

    @property
    def id(self):
        # type: () -> str
        """
        Block type name
        """
        return self.__id


class Block(object):
    """
    Represents a block in a dimension. 
    A block represents a unique X, Y, and Z within a dimension and get/sets the state of the block at that location.
    """

    def __init__(self, data):
        self.__dimension = data['dimension']
        self.__location = data['location']
        self.__typeId = data['typeId']
        self.__permutation = data['permutation']
        self.__isAir = True if self.__typeId == 'minecraft:air' else False
        self.__isLiquid = 

    
