# -*- coding: utf-8 -*-
# from typing import List, Dict, Union
from typing import TypedDict
from ..modules.server.Entity import *

class ExplosionOptions(TypedDict):
    """Additional configuration options for the @minecraft/server.Dimension.createExplosion method."""

    source: Entity
    allowUnderwater: bool
    breaksBlocks: bool
    causesFire: bool

