# -*- coding: utf-8 -*-

from copy import deepcopy
import mod.server.extraServerApi as serverApi
import random
comp = serverApi.GetEngineCompFactory().CreateBlockState(serverApi.GetLevelId())

class BlockPaletteData(object):
    """Process block palette data"""

    def __init__(self, data, copyData=True):
        # type: (dict, bool) -> None
        self.__data = deepcopy(data) if copyData else data
        
        """{
            'extra': {
                ('minecraft:water', 0): [4]
            }, 
            'void': False, 
            'actor': {}, 
            'volume': (3, 2, 1), // z, x, y
            'common': {
                ('minecraft:normal_stone_stairs', 0): [3], 
                ('minecraft:normal_stone_stairs', 1): [1, 5], 
                ('minecraft:normal_stone_stairs', 2): [4]
            }, 
            'eliminateAir': True
        }
        """
        """{
            'extra': {}, 
            'void': False, 
            'actor': {}, 
            'volume': (3, 2, 1), // Real size: 2, 1, 3
            'common': {
                ('minecraft:lapis_block', 0): [4], 
                ('minecraft:emerald_block', 0): [2], 
                ('minecraft:gold_block', 0): [1], 
                ('minecraft:diamond_block', 0): [3], 
                ('minecraft:iron_block', 0): [0], 
                ('minecraft:raw_copper_block', 0): [5]
            }, 
            'eliminateAir': True
        }
        """
        self.__volume = self.__data['volume'] # type: tuple[int, int, int] 
        self.__blocks = self.__data['common'] # type: dict[tuple[str, int], list[int]]
        self.__extra = self.__data['extra'] # type: dict[tuple[str, int], list[int]]
        self.__exludeAirData = ("minecraft:air", 0) not in self.__blocks

    def getExtraBlock(self, location): 
        # type: (tuple[int, int, int]) -> tuple[str, int] | None
        """Returns extra block data in this location. Extra blocks are blocks that are not necessary for the structure to be valid, but may be used for additional details. For example, when a structure is created from the world, water and lava blocks will be categorized as extra blocks."""
        locId = self.getLocationId(location)
        if locId < 0:
            raise ValueError("location is not exist in this palette!")
        for (blockType, blockAux) in self.__extra:
            if locId in self.__extra[(blockType, blockAux)]:
                return (blockType, blockAux)
        return None
    
    def getLocationId(self, location):
        # type: (tuple[int, int, int]) -> int
        """Returns the id of this location, or -1 if this location doesn't exist."""
        if location[0] >= self.__volume[1] or location[1] >= self.__volume[2] or location[2] >= self.__volume[0]:
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

    def setExtraBlock(self, location, blockData):
        locId = self.getLocationId(location)
        if locId < 0:
            return False
        if blockData not in self.__extra:
            self.__extra[blockData] = []
        self.__extra[blockData].append(locId)
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

    def replaceBlocks(self, oldBlockData, newBlockData, v=None):
        """Replace block."""
        if not v:
            v = self.__blocks
        if oldBlockData not in v:
            return
        if newBlockData not in v:
            v[newBlockData] = v[oldBlockData]
        else:
            v[newBlockData] += v[oldBlockData]
        del v[oldBlockData]

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
    
    def rotate(self, rotation):
        if rotation % 90:
            rotation -= rotation % 90
        rotation %= 360
        if not rotation:
            return
        for blockName in self.__data['actor']:
            temp = {}
            for locId in self.__data['actor'][blockName].keys():
                newLocation = self.rotateLocation(self.getLocation(locId), rotation)
                if rotation % 180:
                    newLocId = newLocation[0] * self.__volume[1] + newLocation[1] * self.__volume[0] * self.__volume[1] + newLocation[2]
                else:
                    newLocId = self.getLocationId(newLocation)
                temp[newLocId] = self.__data['actor'][blockName][locId]
            self.__data['actor'][blockName] = temp
        for vk in ["extra", "common"]:
            v = self.__data[vk]
            def replaceBlocks(blockData, newBlockData):
                tempData[newBlockData] = v[blockData]
            tempData = {}

            for blockData in v.keys():
                locations = v[blockData]
                # Rotate block locations
                for i in range(len(locations)):
                    locId = locations[i]
                    location = self.getLocation(locId)
                    newLocation = self.rotateLocation(location, rotation)
                    if rotation % 180:
                        newLocId = newLocation[0] * self.__volume[1] + newLocation[1] * self.__volume[0] * self.__volume[1] + newLocation[2]
                    else:
                        newLocId = self.getLocationId(newLocation)
                    locations[i] = newLocId
                
                # Rotate block directions
                states = comp.GetBlockStatesFromAuxValue(blockData[0], blockData[1])
                if states:
                    # Axis Alignment (e.g. logs)
                    if "pillar_axis" in states:
                        if states['pillar_axis'] == "x":
                            replaceBlocks(blockData, (blockData[0], 2 if rotation % 180 else 1))
                        elif states['pillar_axis'] == "z":
                            replaceBlocks(blockData, (blockData[0], 1 if rotation % 180 else 2))
                        else:
                            tempData[blockData] = v[blockData]
                    # Weirdo directions (e.g. stairs)
                    elif "weirdo_direction" in states:
                        DIRECTIONS = [0, 3, 1, 2]
                        replaceBlocks(blockData, (
                            blockData[0], 
                            DIRECTIONS[(
                                DIRECTIONS.index(
                                    states['weirdo_direction']
                                ) + rotation // 90) % 4
                            ] + (
                                4 if states['upside_down_bit'] else 0
                            )))
                    elif "facing_direction" in states:
                        DIRECTIONS = [2, 4, 3, 5]
                        replaceBlocks(blockData, (blockData[0], DIRECTIONS[(
                                DIRECTIONS.index(
                                    states['facing_direction']
                                ) + rotation // 90) % 4
                            ]))
                    elif "minecraft:cardinal_direction" in states:
                        DIRECTIONS = [1, 0, 3, 2]
                        replaceBlocks(blockData, (blockData[0], DIRECTIONS[(
                                DIRECTIONS.index(
                                    blockData[1]
                                ) + rotation // 90) % 4
                            ]))
                    elif "direction" in states:
                        DIRECTIONS = [2, 0, 3, 1]
                        states['direction'] = DIRECTIONS[(DIRECTIONS.index(states['direction']) + rotation // 90) % 4]
                        replaceBlocks(blockData, (blockData[0], comp.GetBlockAuxValueFromStates(blockData[0], states)))
                    else:
                        tempData[blockData] = v[blockData]
                else:
                    tempData[blockData] = v[blockData]
            self.__data[vk] = tempData
        for blockName in self.__data['actor']:
            DIRECTIONS = [5, 2, 4, 3]
            for locId in self.__data['actor'][blockName]:
                blockData = self.__data['actor'][blockName][locId]
                if "facingDirection" in blockData:
                    for bld in self.__data['common']:
                        if bld[0] == blockName and locId in self.__data['common'][bld]:
                            blockData['facingDirection'] = DIRECTIONS[bld[1]]
                            break
    
        if rotation % 180:
            self.__data['volume'] = (self.__volume[1], self.__volume[0], self.__volume[2])
        self.__blocks = self.__data['common']
        self.__extra = self.__data['extra']

    def rotateLocation(self, location, rotation):
        if rotation == 90:
            return (location[2], location[1], self.__volume[1] - location[0] - 1)
        elif rotation == 180:
            return (self.__volume[1] - location[0] - 1, location[1], self.__volume[0] - location[2] - 1)
        elif rotation == 270:
            return (self.__volume[0] - location[2] - 1, location[1], location[0])

    def mirror(self, mirrorAxis):
        # type: (str) -> None
        for vk in ["extra", "common"]:
            v = self.__data[vk]
            def replaceBlocks(blockData, newBlockData):
                tempData[newBlockData] = v[blockData]
            tempData = {}

            for blockData in v:
                locations = v[blockData]
                for i in range(len(locations)):
                    locId = locations[i]
                    location = self.getLocation(locId)
                    newLocation = (
                        (self.__volume[1] - location[0] - 1 if 'Z' in mirrorAxis else location[0]), 
                        location[1], 
                        (self.__volume[0] - location[2] - 1 if 'X' in mirrorAxis else location[2])
                    )
                    locations[i] = self.getLocationId(newLocation)

                # Mirror block directions
                states = comp.GetBlockStatesFromAuxValue(blockData[0], blockData[1])
                if states:
                    shouldMirror = False
                    # Weirdo directions (e.g. stairs)
                    if "weirdo_direction" in states:
                        DIRECTIONS = [0, 3, 1, 2]
                        if "Z" in mirrorAxis and DIRECTIONS.index(states['weirdo_direction']) % 2:
                            shouldMirror = True
                        elif "X" in mirrorAxis and not DIRECTIONS.index(states['weirdo_direction']) % 2:
                            shouldMirror = True
                        replaceBlocks(blockData, (
                            blockData[0], 
                            DIRECTIONS[(
                                DIRECTIONS.index(
                                    states['weirdo_direction']
                                ) + (2 if shouldMirror else 0)) % 4
                            ] + (
                                4 if states['upside_down_bit'] else 0
                            )))
                    elif "facing_direction" in states:
                        DIRECTIONS = [2, 4, 3, 5]
                        if "Z" in mirrorAxis and DIRECTIONS.index(states['facing_direction']) % 2:
                            shouldMirror = True
                        elif "X" in mirrorAxis and not DIRECTIONS.index(states['facing_direction']) % 2:
                            shouldMirror = True
                        replaceBlocks(blockData, (blockData[0], DIRECTIONS[(
                                DIRECTIONS.index(
                                    states['facing_direction']
                                ) + (2 if shouldMirror else 0)) % 4
                            ]))
                    elif "minecraft:cardinal_direction" in states:
                        DIRECTIONS = [1, 0, 3, 2]
                        if "X" in mirrorAxis and DIRECTIONS.index(blockData[1]) % 2:
                            shouldMirror = True
                        elif "Z" in mirrorAxis and not DIRECTIONS.index(blockData[1]) % 2:
                            shouldMirror = True
                        replaceBlocks(blockData, (blockData[0], DIRECTIONS[(
                                DIRECTIONS.index(
                                    blockData[1]
                                ) + (2 if shouldMirror else 0)) % 4
                            ]))
                    elif "direction" in states:
                        DIRECTIONS = [2, 0, 3, 1]
                        if "Z" in mirrorAxis and DIRECTIONS.index(states['direction']) % 2:
                            shouldMirror = True
                        elif "X" in mirrorAxis and not DIRECTIONS.index(states['direction']) % 2:
                            shouldMirror = True
                        states['direction'] = DIRECTIONS[(DIRECTIONS.index(states['direction']) + (2 if shouldMirror else 0)) % 4]
                        replaceBlocks(blockData, (blockData[0], comp.GetBlockAuxValueFromStates(blockData[0], states)))
                    else:
                        tempData[blockData] = v[blockData]
                else:
                    tempData[blockData] = v[blockData]
            self.__data[vk] = tempData
        for blockName in self.__data['actor']:
            DIRECTIONS = [5, 2, 4, 3]
            for locId in self.__data['actor'][blockName]:
                blockData = self.__data['actor'][blockName][locId]
                if "facingDirection" in blockData:
                    for bld in self.__data['common']:
                        if bld[0] == blockName and locId in self.__data['common'][bld]:
                            blockData['facingDirection'] = DIRECTIONS[bld[1]]
                            break
        
        self.__blocks = self.__data['common']
        self.__extra = self.__data['extra']
    
    def damage(self, seed, integrity):
        """Apply integrity."""
        base = integrity / 100.0
        for v in [self.__extra, self.__blocks]:
            for blockData in v:
                # Damage blocks
                locations = v[blockData]
                for locId in locations:
                    random.seed(seed + locId)
                    if random.random() + base < 1:
                        locations.remove(locId)

    def clearExtraWater(self):
        for blockData in self.__extra:
            if blockData[0] == "minecraft:water":
                del self.__extra[blockData]     

    def fillVoid(self):
        """Fill void blocks to air."""
        if not self.__exludeAirData:
            return
        blocks = []
        for blockData in self.__blocks:
            blocks += self.__blocks[blockData]
        maxNum = self.__volume[0] * self.__volume[1] * self.__volume[2] - 1
        air = []
        for locId in range(maxNum):
            if locId not in blocks:
                air.append(locId)
        self.__blocks[("minecraft:air", 0)] = air
    
    def clearStructureVoid(self):
        """Clear structure void blocks."""
        if ("minecraft:structure_void", 0) in self.__blocks:
            del self.__blocks[("minecraft:structure_void", 0)]

    def setSize(self):
        """"""
        
