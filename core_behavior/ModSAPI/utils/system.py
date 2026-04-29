# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi

class Systems:

    _world = None
    _modules = None
    _system = None
    _enums = None
    _core = None
    _components = None

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
    def core(self):
        if self._core:
            return self._core
        core = serverApi.GetSystem("ModSAPI", "core")
        self._core = core
        return core
    
    @property
    def modules(self):
        if self._modules:
            return self._modules
        modules = serverApi.GetSystem("ModSAPI", "modules")
        self._modules = modules
        return modules
    
    @property
    def enums(self):
        if self._enums:
            return self._enums
        enums = serverApi.GetSystem("ModSAPI", "enums")
        self._enums = enums
        return enums
    
    @property
    def components(self):
        if self._components:
            return self._components
        components = serverApi.GetSystem("ModSAPI", "components")
        self._components = components
        return components
    
systems = Systems()