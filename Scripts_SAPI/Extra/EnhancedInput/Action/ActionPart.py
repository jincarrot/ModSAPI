# -*- coding: utf-8 -*-
from Preset.Model.PartBase import PartBase
from Preset.Model.GameObject import registerGenericClass
import mod.client.extraClientApi as clientApi
import mod.server.extraServerApi as serverApi
from ..EnhancedInput.EnhancedInputPart import ActionEvent, ActionEventType, EnhancedInput

class ValueType:
    Bool = 1
    Float = 2
    Vector2 = 3
    Vector3 = 4

class ModifierType:
    Clamp = 1
    Negate = 2
    Deadzone = 3
    Scalar = 4

class Modifier:
    def __init__(self, modifier):
        self.type = modifier['type']
        self.clamp = modifier['clamp']
        self.negate = modifier['negate']
        self.deadzone = modifier['deadzone']
        self.scalar = modifier['scalar']
    
    def Get(self, index):
        if self.type == ModifierType.Clamp:
            return self.clamp[min(index, len(self.clamp) - 1)]
        elif self.type == ModifierType.Negate:
            return self.negate[min(index, len(self.negate) - 1)]
        elif self.type == ModifierType.Deadzone:
            return self.deadzone[min(index, len(self.deadzone) - 1)]
        elif self.type == ModifierType.Scalar:
            return self.scalar[min(index, len(self.scalar) - 1)]
        else:
            return 0
        
    def Size(self):
        if self.type == ModifierType.Clamp:
            return len(self.clamp)
        elif self.type == ModifierType.Negate:
            return len(self.negate)
        elif self.type == ModifierType.Deadzone:
            return len(self.deadzone)
        elif self.type == ModifierType.Scalar:
            return len(self.scalar)
        else:
            return 0

@registerGenericClass("ActionPart")
class ActionPart(PartBase):
    def __init__(self):
        super(ActionPart, self).__init__()
        # 零件名称
        self.name = "动作"
        self.action = ""
        self.allowServer = True
        self.allowClient = True
        self.valueType = 1
        self.modifiers = []

    def InitClient(self):
        PartBase.InitClient(self)
        self.RegisterToEnhancedInputClient()

    def InitServer(self):
        PartBase.InitServer(self)
        self.RegisterToEnhancedInput()

    def RegisterToEnhancedInput(self):
        EnhancedInputPart = self.GetParent().GetPartByType('EnhancedInputPart')
        if self.allowServer:
            self.ListenPartEvent(
                EnhancedInputPart.id,
                EnhancedInput.Action(self.action),
                self,
                self.HandleActionServer
            )

    def RegisterToEnhancedInputClient(self):
        EnhancedInputPart = self.GetParent().GetPartByType('EnhancedInputPart')
        if self.allowClient:
            self.ListenPartEvent(
                EnhancedInputPart.id,
                EnhancedInput.Action(self.action),
                self,
                self.HandleAction
            )

    def HandleAction(self, event):
        # type: (ActionEvent) -> None
        Event = ActionEvent.FromEventData(event)
        EventHandlerName = 'On' + ActionEventType.GetState(Event.eventType)
        if hasattr(self, EventHandlerName):
            getattr(self, EventHandlerName)(self.GetValue(Event.value))

    def HandleActionServer(self, event):
        # type: (ActionEvent) -> None
        Event = ActionEvent.FromEventData(event)
        EventHandlerName = 'On' + ActionEventType.GetState(Event.eventType) + 'Server'
        if hasattr(self, EventHandlerName):
            getattr(self, EventHandlerName)(self.GetValue(Event.value))

    def TransferValue(this, value):
        # type: (tuple[float, float, float]) -> any
        if this.valueType == ValueType.Vector3:
            return value
        elif this.valueType == ValueType.Vector2:
            return (value[0], value[1])
        elif this.valueType == ValueType.Float:
            return value[0]
        elif this.valueType == ValueType.Bool:
            return value[0] ** 2 + value[1] ** 2 + value[2] ** 2 > 0.0001
        
    def ApplyModifier(self, value, modifier):
        # type: (tuple[float, float, float], Modifier) -> tuple[float, float, float]
        m = Modifier(modifier)

        if m.Size() == 0:
            return value

        if m.type == ModifierType.Clamp:
            return self._ApplyClamp(value, m)
        elif m.type == ModifierType.Deadzone:
            return self._ApplyDeadzone(value, m)
        elif m.type == ModifierType.Negate:
            return self._ApplyNegate(value, m)
        elif m.type == ModifierType.Scalar:
            return self._ApplyScalar(value, m)

    def _ApplyClamp(self, value, modifier):
        # type: (tuple[float, float, float], Modifier) -> tuple[float, float, float]
        return (
            max(min(value[0], modifier.Get(0)['max']), modifier.Get(0)['min']),
            max(min(value[1], modifier.Get(1)['max']), modifier.Get(1)['min']),
            max(min(value[2], modifier.Get(2)['max']), modifier.Get(2)['min'])
        )
    
    def _ApplyDeadzone(self, value, modifier):
        # type: (tuple[float, float, float], Modifier) -> tuple[float, float, float]
        return (
            max(value[0], modifier.Get(0)),
            max(value[1], modifier.Get(1)),
            max(value[2], modifier.Get(2))
        )
    
    def _ApplyNegate(self, value, modifier):
        # type: (tuple[float, float, float], Modifier) -> tuple[float, float, float]
        return (
            -value[0] if modifier.Get(0) else value[0],
            -value[1] if modifier.Get(1) else value[1],
            -value[2] if modifier.Get(2) else value[2]
        )

    def _ApplyScalar(self, value, modifier):
        # type: (tuple[float, float, float], Modifier) -> tuple[float, float, float]
        return (
            value[0] * modifier.Get(0),
            value[1] * modifier.Get(1),
            value[2] * modifier.Get(2)
        )
    
    def GetValue(self, value):
        for modifier in self.modifiers:
            value = self.ApplyModifier(value, modifier)
        return self.TransferValue(value)
