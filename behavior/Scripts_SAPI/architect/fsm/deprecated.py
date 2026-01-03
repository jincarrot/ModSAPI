# -*- coding: utf-8 -*-

"""
TODO: 临时设计的经典 FSM 框架，不要在ECS中尝试嵌入
"""

from ..unreliable import Unreliable
from ..basic import compClient, compServer, isServer
from mod.common.minecraftEnum import AttrType, EntityType

class State:
    def __init__(self, fsm):
        self.entityId = fsm.entityId
        self.fsm = fsm # type: Fsm
        self.stateTime = 0

    def onEnter(self):
        pass

    def onExit(self):
        pass

    def onUpdate(self):
        pass

    def canEnter(self):
        return True
    
    def getFsm(self):
        return self.fsm
    
    def markVariant(self, value=None):
        compFact = compServer if isServer() else compClient
        defs = compFact.CreateEntityDefinitions(self.entityId)
        if value is None:
            return defs.GetMarkVariant()
        else:
            defs.SetMarkVariant(value)

    def movement(self, enabled=True):
        if not isServer():
            return
        compServer.CreateCommand(self.entityId).SetCommand(
            'inputpermission set @s movement {}'.format('enabled' if enabled else 'disabled'),
            self.entityId
        )
        compServer.CreateEntityEvent(self.entityId).TriggerCustomEvent(self.entityId, 'add_movable' if enabled else 'remove_movable')
        if compServer.CreateEngineType(self.entityId).GetEngineType() != EntityType.Player:
            if enabled:
                compServer.CreateAttr(self.entityId).ResetToDefaultValue(AttrType.SPEED)
            else:
                compServer.CreateAttr(self.entityId).SetAttrValue(AttrType.SPEED, 0.01)

    def camera(self, enabled=True):
        if not isServer():
            return
        compServer.CreateCommand(self.entityId).SetCommand(
            'inputpermission set @s camera {}'.format('enabled' if enabled else 'disabled'),
            self.entityId
        )


class Fsm(Unreliable):
    def __init__(self, defaultState, name='default'):
        Unreliable.__init__(self)
        self.states = {
            name: defaultState
        }
        self.defaultState = defaultState # type: State
        self.currentState = defaultState # type: State
        self.currentStateName = name # type: str
        self.defaultStateName = name # type: str

    def addState(self, name, stateCls):
        self.states[name] = stateCls(self)

    def addStateMapping(self, states):
        for stateName, stateCls in states.items():
            self.addState(stateName, stateCls)

    def getState(self, name):
        return self.states[name]

    def transitionTo(self, name):
        state = self.states[name]
        if state.canEnter():
            if self._callExit(self.currentState):
                if name != 'default':
                    print(self.currentStateName, '->', name)
                self.currentState = state
                self.currentStateName = name
                return self._callEnter(self.currentState)
        return False


    def _callExit(self, state):
        try:
            state.onExit()
            return True
        except Exception:
            self.currentState = self.defaultState
            return False

    def _callEnter(self, state):
        try:
            state.onEnter()
            state.stateTime = 0
            return True
        except Exception:
            self.currentState = self.defaultState
            return False

    def callUpdate(self):
        self.currentState.stateTime += 1
        self.tryCall(self.currentState.onUpdate)