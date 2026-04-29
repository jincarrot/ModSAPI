# -*- coding: utf-8 -*-
from ...interfaces.EntityOptions import *
from ...interfaces.Vector import *
from ...interfaces.ParticleOptions import *
from .Entity import ClientEntity

class Particle:
    "Contains a set of operations about particle effects."

    @property
    def id(self) -> int:
        """Runtime identifier of this particle effect."""
    
    @property
    def isValid(self) -> bool:
        """Whether this particle effect is valid."""

    @property
    def isBinding(self) -> bool:
        """Whether this particle effect is currently binding to an entity."""

    @property
    def location(self) -> Vector3:
        """Location of this particle effect."""
    
    def bindToEntity(self, entity: ClientEntity, options: ParticleBindEntityOptions = {}) -> bool:
        """Bind this particle effect to an entity. The particle effect will move together with the entity."""

    def getMolang(self, molangExpression: str):
        """Get value of molang."""

    def setMolang(self, molang: str, value):
        """Set value of molang."""
    
    def remove(self):
        """Remove this particle effect."""
        