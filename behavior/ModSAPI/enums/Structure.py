
STRUCTUREANIMATIONS = [
    "None",
    "Layers",
    "Blocks"
]


STRUCTUREMIRRORS = [
    "None",
    "X",
    "Z",
    "XZ"
]


class StructureSaveMode:
    """
    Specifies how a structure should be saved.
    """

    Memory = 0
    """
    The structure will be temporarily saved to memory. 
    The structure will persist until the world is shut down.
    """

    World = 1
    """
    The structure will be saved to the world file and persist between world loads. 
    A saved structure can be removed from the world via @minecraft/server.StructureManager.delete.
    """


class StructureMirrorAxis:
    """
    Specifies how a structure should be mirrored when placed.
    """

    none = "None"
    """No mirroring."""

    X = "X"
    """Structure is mirrored across the X axis."""

    Z = "Z"
    """Structure is mirrored across the Z axis."""

    XZ = "XZ"
    """Structure is mirrored across both the X and Z axis."""


class StructureRotation:
    """
    Enum describing a structure's placement rotation.
    """

    none = "None"
    """No rotation."""

    Rotate90 = "Rotate90"
    """90 degree rotation."""

    Rotate180 = "Rotate180"
    """180 degree rotation."""

    Rotate270 = "Rotate270"
    """270 degree rotation."""


class StructureAnimationMode:
    """Specifies how structure blocks should be animated when a structure is placed."""

    Blocks = "Blocks"
    """
    Blocks will be randomly placed one at at time. 
    Use @minecraft/server.StructurePlaceOptions.animationSeconds to control how long it takes for all blocks to be placed.
    """

    Layers = "Layers"
    """
    Blocks will be placed one layer at a time from bottom to top. 
    Use @minecraft/server.StructurePlaceOptions.animationSeconds to control how long it takes for all blocks to be placed.
    """

    none = "None"
    """
    All blocks will be placed immediately.
    """