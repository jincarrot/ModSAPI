# -*- coding: utf-8 -*-
# from typing import List, Dict, Union
from ..Classes.Block import *


class BlockFilter(object):
    """
    Options to include or exclude blocks based on type, tag or permutation. 
    If no include options are added it will select all blocks that are not rejected by the exclude options. 
    If at least one include option is added the block must match one of the include options to not be rejected.
    """

    def __init__(self, data):
        self.excludePermutations = data['excludePermutations'] if 'excludePermutations' in data else None
        """Array of block permutations that the filter should reject if any matches."""
        self.excludeTags = data['excludeTags'] if 'excludeTags' in data else None
        """Array of block tags that the filter should reject if any matches."""
        self.excludeTypes = data['excludeTypes'] if 'excludeTypes' in data else None
        """Array of block types that the filter should reject if any matches."""
        self.includePermutations = data['includePermutations'] if 'includePermutations' in data else None
        """Array of block permutations that the filter should select if at least one matches."""
        self.includeTags = data['includeTags'] if 'includeTags' in data else None
        """Array of block tags that the filter should select if at least one matches."""
        self.includeTypes = data['includeTypes'] if 'includeTypes' in data else None
        """Array of block types that the filter should select if at least one matches."""


class BlockRaycastOptions(BlockFilter):
    """
    Returns the first intersecting block from the direction that this entity is looking at.
    """

    def __init__(self, data):
        BlockFilter.__init__(self, data)
        self.includeLiquidBlock = data['includeLiquidBlock'] if 'includeLiquidBlock' in data else True
        """If true, the raycast will return a liquid block if it is the first block hit."""
        self.includePassableBlocks = data['includePassableBlocks'] if 'includePassableBlocks' in data else True
        """If true, the raycast will return a passable block if it is the first block hit."""
        self.maxDistance = data['maxDistance'] if 'maxDistance' in data else 32
        """The maximum distance the raycast will check for blocks."""


class BlockEventOptions(object):
    """
    Contains optional parameters for registering a block event.
    """

    def __init__(self, data):
        self.__permutations = data['permutations'] if 'permutations' in data else []
        self.__blockTypes = data['blockTypes'] if 'blockTypes' in data else []

    @property
    def permutations(self):
        # type: () -> list[BlockPermutation]
        """If this value is set, this event will only fire if the impacted block's permutation matches this parameter."""
        return self.__permutations

    @permutations.setter
    def permutations(self, data):
        # type: (list[BlockPermutation]) -> None
        self.__permutations = data

    @property
    def blockTypes(self):
        # type: () -> list[str]
        """If this value is set, this event will only fire if the impacted block's type matches this parameter."""
        return self.__blockTypes

    @blockTypes.setter
    def blockTypes(self, data):
        # type: (list[str]) -> None
        self.__blockTypes = data
