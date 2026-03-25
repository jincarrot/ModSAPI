# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi

class Systems:

    _world = None
    _modules = None
    _system = None

    @property
    def world(self):
        if self._world:
            return self._world
        world = serverApi.GetSystem("ModSAPI", "world")
        self._world = world
        return world
    
    @property
    def system(self):
        if self._system:
            return self._system
        system = serverApi.GetSystem("ModSAPI", "system")
        self._system = system
        return system
    
    @property
    def modules(self):
        if self._modules:
            return self._modules
        modules = serverApi.GetSystem("ModSAPI", "modules")
        self._modules = modules
        return modules
    
systems = Systems()