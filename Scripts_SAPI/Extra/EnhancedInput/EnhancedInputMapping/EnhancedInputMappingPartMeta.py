# -*- coding: utf-8 -*-
from Meta.ClassMetaManager import sunshine_class_meta
from Meta.EnumMeta import DefEnum
from Meta.TypeMeta import PBool, PStr, PInt, PCustom, PVector3, PVector3TF, PEnum, PDict, PFloat, PArray, PVector2, PColor, PObjectArray
from Preset.Model import PartBaseMeta
from Preset.Model.PresetDataMeta import PropertyListObject
from Meta.PropertyObject import sunshine_property_object

KeyBoard = DefEnum("KeyBoard", {
    8: 'Backspace键',
    9: 'Tab键',
    13: '回车键',
    19: 'PAUSE键',

    16: 'SHIFT键',
    17: 'CONTROL键',
    18: 'ALT键',
    20: 'CAPS LOCK键(大小写键)',
    27: 'Esc键',
    32: '空格键',
    33: 'Page Up键',
    34: 'Page Down键',
    35: 'End键',
    36: 'Home键',

    37: '方向左键(←)',
    38: '方向上键(↑)',
    39: '方向右键(→)',
    40: '方向下键(↓)',
    45: 'Insert键',
    46: 'Delete键',

    48: '数字0',
    49: '数字1',
    50: '数字2',
    51: '数字3',
    52: '数字4',
    53: '数字5',
    54: '数字6',
    55: '数字7',
    56: '数字8',
    57: '数字9',

    65: 'A键',
    66: 'B键',
    67: 'C键',
    68: 'D键',
    69: 'E键',
    70: 'F键',
    71: 'G键',
    72: 'H键',
    73: 'I键',
    74: 'J键',
    75: 'K键',
    76: 'L键',
    77: 'M键',
    78: 'N键',
    79: 'O键',
    80: 'P键',
    81: 'Q键',
    82: 'R键',
    83: 'S键',
    84: 'T键',
    85: 'U键',
    86: 'V键',
    87: 'W键',
    88: 'X键',
    89: 'Y键',
    90: 'Z键',

    96: '数字0(小键盘)',
    97: '数字1(小键盘)',
    98: '数字2(小键盘)',
    99: '数字3(小键盘)',
    100: '数字4(小键盘)',
    101: '数字5(小键盘)',
    102: '数字6(小键盘)',
    103: '数字7(小键盘)',
    104: '数字8(小键盘)',
    105: '数字9(小键盘)',
    106: '乘号键(×)(小键盘)',
    107: '加号键(+)(小键盘)',

    109: '减号键(-)',
    110: '小数点(.)',
    111: '除法键(/)',
    112: '功能键F1',
    113: '功能键F2',
    114: '功能键F3',
    115: '功能键F4',
    116: '功能键F5',
    117: '功能键F6',
    118: '功能键F7',
    119: '功能键F8',
    120: '功能键F9',
    121: '功能键F10',
    122: '功能键F11',
    123: '功能键F12',
    124: '功能键F13',

    144: 'Num Lock键',
    145: 'Scroll Lock键',

    186: ': ; 键',
    187: '= + 键',
    188:', < 键',
    189: '- _ 键',
    190: '. > 键',
    191: '/ ? 键',
    192: '` ~ 键',

    219: '[ { 键',
    220: '\ | 键',
    221: '] } 键',
    222: '\' " 键',
})

GamepadKey = DefEnum("GamepadKey", {
    1: 'A键',
    2: 'B键',
    3: 'X键',
    4: 'Y键',
    5: '向上方向键',
    6: '向下方向键',
    7: '向左方向键',
    8: '向右方向键',
    9: 'LS键',
    10: 'RS键',
    11: 'LB键',
    12: 'RB键',
    13: 'VIEW键',
    14: 'MENU键',

    256: '左摇杆',
    257: '右摇杆',

    4096: '左扳机',
    4097: '右扳机',
}) 

TriggerType = DefEnum("TriggerType", {
    1: '按下',
    2: '按住',
    3: '松开',
    4: '组合',
})

InputType = DefEnum("InputType", {
    1: '键盘',
    2: '鼠标',
    3: '手柄',
    4: '事件',
})

MouseInput = DefEnum("MouseInput", {
    1: '左键',
    2: '中键',
    3: '右键',
    4: '滚轮',
})

AxisType = DefEnum("AxisType", {
    4: 'X',
    2: 'Y',
    1: 'Z',
    6: 'XY',
    5: 'XZ',
    3: 'YZ',
    7: 'XYZ',
})

@sunshine_property_object
class InputMeta(PropertyListObject):
    PROPERTIES = {
        'preventDefault': PBool(text='阻止默认行为', default=True),
        'inputType': PEnum(text='输入类型', enumType='InputType'),
        'eventInput': PStr(text='事件输入', func=lambda v: { 'visible': v.inputType == 4 }),
        'mouseInput': PEnum(text='鼠标输入', enumType='MouseInput', func=lambda v: { 'visible': v.inputType == 2 }),
        'keyboardInput': PEnum(text='键盘输入', enumType='KeyBoard', func=lambda v: { 'visible': v.inputType == 1 }),
        'gamepadInput': PEnum(text='手柄输入', enumType='GamepadKey', func=lambda v: { 'visible': v.inputType == 3 }),
        'advanced': PDict(sort=90, text='高级选项', children={
            'axis': PEnum(text='输入到轴', enumType='AxisType'),
            'negate': PDict(text='取反', children={
                'x': PBool(text='X'),
                'y': PBool(text='Y'),
                'z': PBool(text='Z'),
            }),
        }),
    }

@sunshine_property_object
class TriggerMeta(PropertyListObject):
    PROPERTIES = {
        'type': PEnum(text='触发类型', enumType='TriggerType'),
        'hold': PDict(sort=90, text='按住', func=lambda v: { 'visible': v.type == 2 }, children={
            'holdThreshold': PFloat(text='触发时间(s)', default=0.2),
            'actuationThreshold': PFloat(text='持续时间(s)', default=1.5),
        }),
        'combine': PDict(sort=90, text='组合', func=lambda v: { 'visible': v.type == 4 }, children={
            'actuationThreshold': PFloat(text='持续时间(s)', default=0.5),
        }),
    }


@sunshine_class_meta
class EnhancedInputMappingPartMeta(PartBaseMeta):
    CLASS_NAME = "EnhancedInputMappingPart"
    ObjectArrayDef = {
    	"keys": InputMeta,
    	"triggers": TriggerMeta
    }
    PROPERTIES = {
        'action': PStr(sort=90, text='动作id'),
        'broadcastToServer': PBool(sort=92, text='广播到服务器'),
        'keys': PObjectArray(sort=93, text='输入', itemCreator=InputMeta),
        'triggers': PObjectArray(sort=94, text='触发器', itemCreator=TriggerMeta),
    }