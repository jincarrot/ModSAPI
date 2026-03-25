# -*- coding: utf-8 -*-

class BlockPaletteData(object):
    """Process block palette data"""

    def __init__(self, data):
        # type: (dict) -> None
        self.__data = data.copy()
        """{
            'extra': {}, 
            'void': False, 
            'actor': {}, 
            'volume': (3, 3, 2), 
            'common': {
                ('minecraft:light_gray_terracotta', 0): [3], 
                ('minecraft:hardened_clay', 0): [4], 
                ('minecraft:white_terracotta', 0): [1], 
                ('minecraft:orange_terracotta', 0): [8], 
                ('minecraft:brown_terracotta', 0): [7], 
                ('minecraft:gray_terracotta', 0): [13], 
                ('minecraft:black_terracotta', 0): [5], 
                ('minecraft:red_terracotta', 0): [2], 
                ('minecraft:yellow_terracotta', 0): [0]
            }, 
            'eliminateAir': False
        }"""
        self.__volume = self.__data['volume'] # type: tuple[int, int, int]
        self.__blocks = self.__data['common'] # type: dict[tuple[str, int], list[int]]
        self.__exludeAirData = ("minecraft:air", 0) in self.__blocks

    def getLocationId(self, location):
        # type: (tuple[int, int, int]) -> int
        """Returns the id of this location, or -1 if this location doesn't exist."""
        if location[0] >= self.__volume[0] or location[1] >= self.__volume[1] or location[2] >= self.__volume[2]:
            return -1
        else:
            return location[0] * self.__volume[0] + location[1] * self.__volume[0] * self.__volume[1] + location[2]
        
    def getLocation(self, locId):
        # type: (int) -> tuple[int, int, int]
        """Returns the location of this id"""
        sq = self.__volume[0] * self.__volume[1]
        y = locId // sq
        locId %= sq
        x = locId // self.__volume[0]
        z = locId % self.__volume[0]
        return (x, y, z)
    
    def getBlock(self, location):
        # type: (tuple[int, int, int]) -> tuple[str, int]
        """Returns block data in this location"""
        locId = self.getLocationId(location)
        if locId < 0:
            raise ValueError("location is not exist in this palette!")
        for (blockType, blockAux) in self.__blocks:
            if locId in self.__blocks[(blockType, blockAux)]:
                return (blockType, blockAux)
        return ("minecraft:air", 0)
            
    def getLocationIds(self, blockData):
        # type: (tuple[str, int] | str) -> list[int]
        """returns the location ids where this block exist."""
        if type(blockData) == str:
            for (blockType, __aux) in self.__blocks:
                if blockType == blockData:
                    return self.__blocks[(blockType, __aux)]
            return []
        else:
            return self.__blocks.get(blockData, [])
            
    def setBlock(self, location, blockData):
        # type: (tuple[int, int, int], tuple[str, int]) -> bool
        """Set a block in a location."""
        locId = self.getLocationId(location)
        if locId < 0:
            return False
        ori = self.getBlock(location)
        if self.__exludeAirData or ori[0] != "minecraft:air":
            self.__blocks[ori].remove(locId)
            if not self.__blocks[ori]:
                del self.__blocks[ori]
        if blockData not in self.__blocks:
            self.__blocks[blockData] = []
        self.__blocks[blockData].append(locId)
        return True

    def getData(self):
        # type: () -> dict
        """Get data."""
        return self.__data

    def hasBlock(self, blockType, blockAux=-1):
        # type: (str, int) -> bool
        """Returns true if block in this palette, else false."""
        if blockAux >= 0:
            return (blockType, blockAux) in self.__blocks
        else:
            for blockData in self.__blocks.keys():
                if blockType in blockData:
                    return True
        return False

    def replaceBlocks(self, oldBlockData, newBlockData):
        """Replace block."""
        self.__blocks[newBlockData] = self.__blocks[oldBlockData]
        del self.__blocks[oldBlockData]

    def fillBlocks(self, start, end, blockData):
        # type: (tuple[int, int, int], tuple[int, int, int], tuple[str, int]) -> None
        """Fill blocks in a square area."""
        startId = self.getLocationId(start)
        endId = self.getLocationId(end)
        for id in range(min(startId, endId), max(startId, endId) + 1):
            self.setBlock(id, blockData)

    def fillAllBlocks(self, blockData):
        # type: (tuple[str, int]) -> None
        """Fill all blocks in this palatte."""
        maxNum = self.__volume[0] * self.__volume[1] * self.__volume[2]
        data = list(range(maxNum))
        self.__data['common'] = {}
        self.__blocks = self.__data['common']
        self.__blocks[blockData] = data
    