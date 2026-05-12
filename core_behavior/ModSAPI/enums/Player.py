# -*- coding: utf-8 -*-

class PlayerPermissionLevel:
    """The player permission level."""
    Visitor = 0
    """Visitors can only observe the world, not interact with it."""
    Member = 1
    """Members can build and mine, attack players and mobs, and interact with items and entities."""
    Operator = 2
    """Operators can teleport and use commands, in addition to everything Members can do."""
    Custom = 3
    """Custom permission."""

    