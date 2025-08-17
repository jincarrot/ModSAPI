# -*- coding: utf-8 -*-
from Preset.Model.PartBase import PartBase
from Preset.Model.GameObject import registerGenericClass
import mod.client.extraClientApi as clientApi
from time import time
from mod.common.minecraftEnum import KeyBoardType

class EnhancedInput:
    @staticmethod
    def Action(name):
        return 'enhanced_input_' + name

class CopyTrait(object):
    def __init__(self, copyOf, properties):
        # type: (dict, list[str]) -> None
        for key in properties:
            setattr(self, key, copyOf[key])

class TriggerType:
    Pressed = 1
    Hold = 2
    Released = 3
    Combine = 4

class Trigger(CopyTrait):
    properties = ('type', 'hold', 'combine')
    def __init__(self, copyOf):
        super(Trigger, self).__init__(copyOf, self.properties)

class InputType:
    Keyboard = 1
    Mouse = 2
    Gamepad = 3
    Event = 4

class MouseInput:
    Left = 1
    Middle = 2
    Right = 3
    Wheel = 4

InputEvents = (
    'LeftClickBeforeClientEvent',
    'LeftClickReleaseClientEvent',
    'MouseWheelClientEvent',
    'OnMouseMiddleDownClientEvent',
    'RightClickBeforeClientEvent',
    'RightClickReleaseClientEvent',
    'TapOrHoldReleaseClientEvent',

    'OnKeyPressInGame',

    'OnGamepadKeyPressClientEvent',
    'OnGamepadStickClientEvent',
    'OnGamepadTriggerClientEvent',
)

class QueryStateOption:
    action = ''
    mapping = ''
    keyType = 0
    key = -1
    state = -1

    def __init__(
        self,
        action='',
        mapping='',
        keyType=0,
        key=-1,
        state=-1
    ):
        self.action = action
        self.mapping = mapping
        self.keyType = keyType
        self.key = key
        self.state = state

class InputMapping(CopyTrait):
    properties = ('inputType', 'preventDefault', 'eventInput', 'mouseInput', 'keyboardInput', 'gamepadInput', 'advanced')
    def __init__(self, copyOf):
        super(InputMapping, self).__init__(copyOf, self.properties)

    def GetValue(self):
        if self.inputType == InputType.Mouse:
            return self.mouseInput
        elif self.inputType == InputType.Keyboard:
            return self.keyboardInput
        elif self.inputType == InputType.Gamepad:
            return self.gamepadInput
        elif self.inputType == InputType.Event:
            return self.eventInput
        return None

    def _Negate(self, value, negate):
        if not negate:
            return value
        
        return not value if isinstance(value, bool) else -value
    
    def GetModifiedValue(self, value):
        Advanced = self.advanced
        Axis = Advanced['axis']
        Negate = Advanced['negate']
        NegateX = Negate['x']
        NegateY = Negate['y']
        NegateZ = Negate['z']
        Value = (0, 0, 0)
        MaskX = Axis & 4
        MaskY = Axis & 2
        MaskZ = Axis & 1
        if Axis == 4 or Axis == 2 or Axis == 1:
            if MaskX:
                Value = (self._Negate(value, NegateX), 0, 0)
            elif MaskY:
                Value = (0, self._Negate(value, NegateY), 0)
            elif MaskZ:
                Value = (0, 0, self._Negate(value, NegateZ))
            return Value

        for i in range(3):
            vIndex = 0
            if Axis & (1 << i):
                Value[i] = self._Negate(value[vIndex], Negate['x' if i == 0 else 'y' if i == 1 else 'z'])
                vIndex += 1
        
        return Value

class ActionMapping:
    def __init__(self, triggers, action, keys, broadcastToServer):
        self.triggers = triggers
        self.action = action
        self.keys = keys
        self.broadcastToServer = broadcastToServer

class CancelableEvent:
    cancel = False

class MouseWheelEvent:
    direction = 0

class InputState:
    Pressed = 1
    Released = 0

class ActionStates:
    Disuse = 0
    Triggered = 1
    Ongoing = 2

class ActionEventType:
    Started = 1
    Canceled = 2
    Triggered = 3
    Completed = 4
    Ongoing = 5
    Triggering = 6
    Error = 7
    Inactivated = 8

    @staticmethod
    def GetState(eventType):
        if eventType == ActionEventType.Started:
            return "Started"
        elif eventType == ActionEventType.Canceled:
            return "Canceled"
        elif eventType == ActionEventType.Triggered:
            return "Triggered"
        elif eventType == ActionEventType.Completed:
            return "Completed"
        elif eventType == ActionEventType.Ongoing:
            return "Ongoing"
        elif eventType == ActionEventType.Triggering:
            return "Triggering"
        elif eventType == ActionEventType.Error:
            return "Error"
        elif eventType == ActionEventType.Inactivated:
            return "Inactivated"
        return "Unknown"


class ActionEvent:
    def __init__(self, action, value, eventType):
        # type: (str, tuple[float, float, float], ActionEventType) -> None
        self.action = action
        self.value = value
        self.eventType = eventType

    def ToEventData(self):
        return {
            'action': self.action,
            'value': self.value,
            'eventType': self.eventType
        }
    
    @staticmethod
    def FromEventData(data):
        return ActionEvent(data['action'], data['value'], data['eventType'])

class InputNode:
    state = ActionStates.Disuse
    trigger = None

    def __init__(
        self,
        input,
        action,
        value,
        mapping,
        time,
    ):
        # type: (InputMapping, str, tuple[float, float, float], ActionMapping, float) -> None
        self.action = action
        self.value = value
        self.time = time
        self.mapping = mapping
        self.input = input
            
class MappingContext:
    def __init__(self, contextId):
        self.contextId = contextId
        self.inputMapping = []

class ReleasableEvent:
    def __init__(self):
        self.isDown = 0

class KeyEvent:
    def __init__(self):
        self.key = 0

class KeyPressEvent(ReleasableEvent, KeyEvent):
    pass

class Vec2InputEvent(KeyEvent):
    def __init__(self):
        super(Vec2InputEvent, self).__init__()
        self.x = 0.0
        self.y = 0.0

class FloatInputEvent(KeyEvent):
    def __init__(self):
        super(FloatInputEvent, self).__init__()
        self.magnitude = 0.0

class ContextMapping:
    def __init__(self):
        self.contextId = ""
        self.inputMapping = []

StateMap = {
    (ActionStates.Disuse, ActionStates.Disuse): ActionEventType.Inactivated,
    (ActionStates.Ongoing, ActionStates.Ongoing): ActionEventType.Ongoing,
    (ActionStates.Triggered, ActionStates.Triggered): ActionEventType.Triggering,
    (ActionStates.Disuse, ActionStates.Ongoing): ActionEventType.Started,
    (ActionStates.Disuse, ActionStates.Triggered): ActionEventType.Triggered,
    (ActionStates.Ongoing, ActionStates.Disuse): ActionEventType.Canceled,
    (ActionStates.Ongoing, ActionStates.Triggered): ActionEventType.Triggered,
    (ActionStates.Triggered, ActionStates.Disuse): ActionEventType.Completed,
    (ActionStates.Triggered, ActionStates.Ongoing): ActionEventType.Error
}

class InputStateStack(list):
    def Append(self, element):
        # type: (InputNode) -> None
        self.append(element)

    def Pop(self):
        if len(self) > 0:
            return self.pop()
        return None

    def Peek(self):
        if len(self) > 0:
            return self[-1]
        return None
    
    def Remove(self, element):
        if element in self:
            self.remove(element)

    def Find(self, action, input):
        for node in self:
            if node.action == action and node.input.inputType == input.inputType:
                return node
        return None
    
    def Filter(self, fn):
        # type : (Callable[[InputNode], bool]) -> list[InputNode]
        Value = []
        for node in self:
            if fn(node):
                Value.append(node)
        return Value



@registerGenericClass("EnhancedInputPart")
class EnhancedInputPart(PartBase):
    def __init__(self):
        super(EnhancedInputPart, self).__init__()
        self.name = "增强输入"
        self.mappingConf = []
        self.mappingContext = []
        self.etsFiles = []
        self.currentMapping = []
        self.inputStateStack = None
        self.contextUsing = ''
        self.broadcastToServers = set()

    def InitClient(self):
        """
        @description 客户端的零件对象初始化入口
        """
        PartBase.InitClient(self)
        self.FindAvailableMapping()
        self.ListenAllEvents()
        self.TryActivateDefault()

    def TryActivateDefault(self):
        self.UseMapping('Default')

    def FindAvailableMapping(self):
        Parent = self.GetParent()
        for mapping in self.mappingConf:
            inputMapping = mapping['inputMapping']
            mappingContext = MappingContext(mapping['contextId'])
            for mappingStr in inputMapping:
                inputMapping = Parent.GetPartByName(mappingStr)
                mappingContext.inputMapping.append(ActionMapping(
                    inputMapping.Triggers(),
                    inputMapping.Action(),
                    inputMapping.Keys(),
                    inputMapping.BroadcastToServer(),
                ))
                self.mappingContext.append(mappingContext)

    def ListenAllEvents(self):
        ns = clientApi.GetEngineNamespace()
        sysName = clientApi.GetEngineSystemName()

        for EventName in InputEvents:
            self.ListenForEvent(
                ns,
                sysName,
                EventName,
                self,
                getattr(self, '_' + EventName)
            )

    def ResetStack(self):
        self.inputStateStack = InputStateStack()

    def UseMapping(self, id):
        self.ResetStack()
        self.currentMapping = []
        self.broadcastToServers = set()

        for mappingContext in self.mappingContext:
            if mappingContext.contextId == id:
                Mapping = mappingContext.inputMapping
                self.currentMapping = Mapping
                self.contextUsing = id
                for mapping in Mapping:
                    if mapping.broadcastToServer:
                        self.broadcastToServers.add(mapping.action)
                return True
        return False

    def InitServer(self):
        """
        @description 服务端的零件对象初始化入口
        """
        PartBase.InitServer(self)

    def TickClient(self):
        """
        @description 客户端的零件对象逻辑驱动入口
        """
        PartBase.TickClient(self)
        self._UpdateInputStack()

    def TickServer(self):
        """
        @description 服务端的零件对象逻辑驱动入口
        """
        PartBase.TickServer(self)

    def DestroyClient(self):
        """
        @description 客户端的零件对象销毁逻辑入口
        """
        PartBase.DestroyClient(self)

    def DestroyServer(self):
        """
        @description 服务端的零件对象销毁逻辑入口
        """
        PartBase.DestroyServer(self)

    _Comparators = {
        InputType.Event: lambda inputMapping, input: inputMapping.eventInput == input,
        InputType.Keyboard: lambda inputMapping, input: inputMapping.keyboardInput == input,
        InputType.Mouse: lambda inputMapping, input: inputMapping.mouseInput == input,
        InputType.Gamepad: lambda inputMapping, input: inputMapping.gamepadInput == input
    }

    def _Compare(self, inputType, inputMapping, input):
        # type: (InputType, InputMapping, int) -> bool
        return self._Comparators[inputType](inputMapping, input)

    def _FindMatchedMapping(self, inputType, input):
        # type: (InputType, int) -> tuple[InputMapping, ActionMapping]
        for inputMapping in self.currentMapping:
            keys = inputMapping.keys
            for inputSetting in keys:
                inputSettingObj = InputMapping(inputSetting)
                if self._Compare(inputType, inputSettingObj, input):
                    return (inputSettingObj, inputMapping)
        return (None, None)

    # 鼠标事件
    def _LeftClickBeforeClientEvent(self, event):
        # type: (CancelableEvent) -> None
        (input, mapping) = self._FindMatchedMapping(InputType.Mouse, MouseInput.Left)
        if input:
            if input.preventDefault:
                event['cancel'] = True
            self.TriggerAction(
                input,
                input.GetModifiedValue(InputState.Pressed),
                mapping
            )

    def _LeftClickReleaseClientEvent(self, event):
        (input, mapping) = self._FindMatchedMapping(InputType.Mouse, MouseInput.Left)
        if input:
            self.TriggerAction(
                input,
                input.GetModifiedValue(InputState.Released),
                mapping
            )

    def _MouseWheelClientEvent(self, event):
        # type: (MouseWheelEvent) -> None
        # 这个函数暂且有些问题，不使用
        # (input, mapping) = self._FindMatchedMapping(InputType.Mouse, MouseInput.Wheel)
        # if input:
        #     self.TriggerAction(
        #         input,
        #         (event['direction'], 0, 0),
        #         mapping
        #     )
        pass

    def _OnMouseMiddleDownClientEvent(self, event):
        # type: (ReleasableEvent) -> None
        (input, mapping) = self._FindMatchedMapping(InputType.Mouse, MouseInput.Middle)
        if input:
            self.TriggerAction(
                input,
                input.GetModifiedValue(event['isDown']),
                mapping
            )

    def _RightClickBeforeClientEvent(self, event):
        # type: (CancelableEvent) -> None
        (input, mapping) = self._FindMatchedMapping(InputType.Mouse, MouseInput.Right)
        if input:
            if input.preventDefault:
                event['cancel'] = True
            self.TriggerAction(
                input,
                input.GetModifiedValue(InputState.Pressed),
                mapping
            )

    def _TapOrHoldReleaseClientEvent(self, event):
        self._RightClickReleaseClientEvent(event)

    def _RightClickReleaseClientEvent(self, event):
        (input, mapping) = self._FindMatchedMapping(InputType.Mouse, MouseInput.Right)
        if input:
            self.TriggerAction(
                input,
                input.GetModifiedValue(InputState.Released),
                mapping
            )

    # 键盘事件
    def _OnKeyPressInGame(self, event):
        # type: (KeyPressEvent) -> None
        (input, mapping) = self._FindMatchedMapping(InputType.Keyboard, int(event['key']))
        if input:
            if input.GetValue() == KeyBoardType.KEY_F11:
                self.ResetStack()
            self.TriggerAction(
                input,
                input.GetModifiedValue(int(event['isDown'])),
                mapping
            )

    # 游戏手柄事件
    def _OnGamepadKeyPressClientEvent(self, event):
        # type: (KeyPressEvent) -> None
        (input, mapping) = self._FindMatchedMapping(InputType.Gamepad, event['key'])
        if input:
            self.TriggerAction(
                input,
                input.GetModifiedValue(event['isDown']),
                mapping
            )

    def _OnGamepadStickClientEvent(self, event):
        # type: (Vec2InputEvent) -> None
        (input, mapping) = self._FindMatchedMapping(InputType.Gamepad, event['key'])
        if input:
            self.TriggerAction(
                input,
                input.GetModifiedValue((event['x'], event['y'])),
                mapping
            )

    def _OnGamepadTriggerClientEvent(self, event):
        # type: (FloatInputEvent) -> None
        (input, mapping) = self._FindMatchedMapping(InputType.Gamepad, event['key'])
        if input:
            self.TriggerAction(
                input,
                input.GetModifiedValue(event['magnitude']),
                mapping
            )

    def TriggerAction(self, input, value, mapping):
        # type: (InputMapping, tuple[float, float, float], ActionMapping) -> None
        t = time()
        inputNode = InputNode(input, mapping.action, value, mapping, t)
        for trigger in mapping.triggers:
            self._TransTriggeredState(Trigger(trigger), inputNode)

    def _ConsumeInputState(self, inputNode):
        # type: (InputNode) -> None
        self.inputStateStack.Remove(inputNode)

    def _PushInputState(self, inputNode):
        # type: (InputNode) -> None
        self.inputStateStack.Append(inputNode)

    def _FindInputState(self, action, input):
        # type: (str, InputMapping) -> InputNode
        return self.inputStateStack.Find(action, input)
    
    def _FindCuriousInputState(self, curious):
        # type: (InputNode) -> InputNode
        return self._FindInputState(curious.action, curious.input)

    def IsFalsyValue(self, value):
        # type: (tuple[float, float, float]) -> bool
        (x, y, z) = value
        return x ** 2 + y ** 2 + z ** 2 < 0.01
    
    def IsTruthyValue(self, value):
        # type: (tuple[float, float, float]) -> bool
        (x, y, z) = value
        return x ** 2 + y ** 2 + z ** 2 >= 0.01

    def _GetActionStateFromInput(self, inputNode):
        # type: (InputNode) -> ActionStates
        return inputNode.state if inputNode else ActionStates.Disuse
    
    def _GetActionEventType(self, prevInput, state):
        # type: (InputNode, ActionStates) -> ActionEventType
        actionEvent = StateMap.get((
            self._GetActionStateFromInput(prevInput),
            state, 
        ))
        return actionEvent
    
    def _TransTriggeredState(self, trigger, inputNode):
        # type: (Trigger, InputNode) -> bool
        triggerType = trigger.type
        if triggerType == TriggerType.Pressed:
            self._TransStatePressed(inputNode, trigger)
        elif triggerType == TriggerType.Released:
            self._TransStateReleased(inputNode, trigger)
        elif triggerType == TriggerType.Hold:
            self._TransStateHold(inputNode, trigger)
        elif triggerType == TriggerType.Combine:
            self._TransStateCombine(inputNode, trigger)

    def _TransStatePressed(self, inputNode, trigger):
        # type: (InputNode, Trigger) -> ActionEventType
        PrevInputNode = self._FindCuriousInputState(inputNode)

        if PrevInputNode:
            self._ConsumeInputState(PrevInputNode)
            self.BroadcastAction(
                inputNode.action,
                inputNode.value,
                ActionEventType.Completed
            )
        else:
            self._PushInputState(inputNode)
            inputNode.trigger = trigger
            self.BroadcastAction(
                inputNode.action,
                inputNode.value,
                ActionEventType.Started
            )
            self.BroadcastAction(
                inputNode.action,
                inputNode.value,
                ActionEventType.Triggered
            )

    def _TransStateReleased(self, inputNode, trigger):
        # type: (InputNode, Trigger) -> ActionEventType
        PrevInputNode = self._FindCuriousInputState(inputNode)

        if PrevInputNode:
            self._ConsumeInputState(PrevInputNode)
            self.BroadcastAction(
                inputNode.action,
                inputNode.value,
                ActionEventType.Triggered
            )
            self.BroadcastAction(
                inputNode.action,
                inputNode.value,
                ActionEventType.Completed
            )
        else:
            self._PushInputState(inputNode)
            inputNode.trigger = trigger
            self.BroadcastAction(
                inputNode.action,
                inputNode.value,
                ActionEventType.Started
            )

    def _UpdateHoldState(self, inputNode):
        # type: (InputNode) -> None
        Hold = inputNode.trigger.hold
        if not Hold:
            return
        
        DeltaTime = time() - inputNode.time
        HoldThreshold = Hold['holdThreshold']
        ActuationThreshold = Hold['actuationThreshold']
        Progress = (DeltaTime - HoldThreshold) / ActuationThreshold
        if DeltaTime < HoldThreshold:
            pass
        elif DeltaTime < ActuationThreshold + HoldThreshold:
            if inputNode.state != ActionStates.Ongoing:
                inputNode.state = ActionStates.Ongoing
                self.BroadcastAction(
                    inputNode.action,
                    (Progress, 0, 0),
                    ActionEventType.Started
                )
        elif inputNode.state != ActionStates.Triggered:
            inputNode.state = ActionStates.Triggered
            self.BroadcastAction(
                inputNode.action,
                (Progress, 0, 0),
                ActionEventType.Triggered
            )
    
    def _TransStateHold(self, inputNode, trigger):
        # type: (InputNode, Trigger) -> ActionEventType
        PrevInputNode = self._FindCuriousInputState(inputNode)

        if not PrevInputNode:
            self._PushInputState(inputNode)
            inputNode.state = ActionStates.Disuse
            inputNode.trigger = trigger
            inputNode.prevTime = inputNode.time
            return

        self._ConsumeInputState(PrevInputNode)
        DeltaTime = time() - PrevInputNode.time
        Progress = (DeltaTime - trigger.hold['holdThreshold']) / trigger.hold['actuationThreshold']
        self.BroadcastAction(
            inputNode.action,
            (Progress, 0, 0),
            StateMap.get((
                self._GetActionStateFromInput(PrevInputNode),
                ActionStates.Disuse
            ))
        )

    def _UpdateCombineState(self, inputNode):
        # type: (InputNode) -> None
        FirstCombinedInput = None
        FirstInputIndex = 0
        for inputState in self.inputStateStack:
            if inputState.trigger == inputNode.trigger and inputState.action == inputNode.action:
                FirstCombinedInput = inputState
                break
            FirstInputIndex += 1

        if not FirstCombinedInput:
            return
        
        DeltaTime = time() - FirstCombinedInput.time
        CombinedInputs = [ FirstCombinedInput ]
        if DeltaTime > FirstCombinedInput.trigger.combine['actuationThreshold']:
            for i in range(FirstInputIndex + 1, len(self.inputStateStack)):
                inputState = self.inputStateStack[i]
                if inputState.trigger == inputNode.trigger and inputState.action == inputNode.action:
                    CombinedInputs.append(inputState)
        
            for inputState in CombinedInputs:
                self._ConsumeInputState(inputState)
                inputState.state = ActionStates.Triggered

            self.BroadcastAction(
                inputNode.action,
                (0, 0, 0),
                ActionEventType.Canceled
            )

    def _TransStateCombine(self, inputNode, trigger):
        # type: (InputNode, Trigger) -> ActionEventType

        # 只有按下时有效
        if self.IsFalsyValue(inputNode.value):
            return
        
        inputNode.trigger = trigger

        RequiredKeys = inputNode.mapping.keys
        CombinedKeys = []
        CombinedInputNodes = []

        def ClearCombinedInputs():
            for input in CombinedInputNodes:
                self._ConsumeInputState(input)

        for inputState in self.inputStateStack:
            if inputState.trigger.type == trigger.type and inputState.action == inputNode.action:
                CombinedKeys.append(inputState.input)
                CombinedInputNodes.append(inputState)

        CombinedKeys.append(inputNode.input)
        
        if len(RequiredKeys) != len(CombinedKeys):
            self._PushInputState(inputNode)
            return

        ClearCombinedInputs()
        self.BroadcastAction(
            inputNode.action,
            (1, 0, 0),
            ActionEventType.Triggered
        )
        self.BroadcastAction(
            inputNode.action,
            (1, 0, 0),
            ActionEventType.Completed
        )
        
    def _UpdateInputStack(self):
        for inputState in self.inputStateStack:
            if not inputState.trigger:
                continue

            if inputState.trigger.type == TriggerType.Hold:
                self._UpdateHoldState(inputState)
            elif inputState.trigger.type == TriggerType.Combine:
                self._UpdateCombineState(inputState)

    def BroadcastAction(self, action, value, eventType):
        # type: (str, tuple[float, float, float], ActionEventType) -> None
        if eventType == ActionEventType.Inactivated:
            return
        
        Event = ActionEvent(
            action,
            value,
            eventType
        )

        self.BroadcastEvent(
            EnhancedInput.Action(action),
            Event.ToEventData()
        )

        if action in self.broadcastToServers:
            self.NotifyToServer(
                EnhancedInput.Action(action),
                Event.ToEventData()
            )
            
    def QueryState(self, option=QueryStateOption()):
        # type: (QueryStateOption) -> list[InputNode]
        def filter(inputState):
            if option.action and inputState.action != option.action:
                return False
            if option.mapping and inputState.mapping != option.mapping:
                return False
            if option.keyType != -1 and inputState.input.type != option.keyType:
                return False
            if option.key != -1 and inputState.input.key != option.key:
                return False
            if option.state != -1 and inputState.state != option.state:
                return False
            return True

        return self.inputStateStack.Filter(filter)
