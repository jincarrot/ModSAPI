# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi

ServerSystem = serverApi.GetServerSystemCls()

class Components(ServerSystem):
    """Contains all components of ModSAPI."""

    @property
    def EntityEquippableComponent(self):
        from ..modules.server.components.EntityComponents import EntityEquippableComponent as e
        return e
    
    @property
    def EntityInventoryComponent(self):
        from ..modules.server.components.EntityComponents import EntityInventoryComponent as e
        return e
    

