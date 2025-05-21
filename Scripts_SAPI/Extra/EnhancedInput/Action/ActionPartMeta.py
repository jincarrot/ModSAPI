# -*- coding: utf-8 -*-
from Meta.ClassMetaManager import sunshine_class_meta
from Meta.EnumMeta import DefEnum
from Meta.TypeMeta import PBool, PStr, PInt, PCustom, PVector3, PVector3TF, PEnum, PDict, PFloat, PArray, PVector2, PColor, PObjectArray
from Preset.Model import PartBaseMeta
from Preset.Model.PresetDataMeta import PropertyListObject
from Meta.PropertyObject import sunshine_property_object

ValueType = DefEnum("ValueType", {
    1: "布尔",      #"Bool",
    2: "浮点",      #"Float",
    3: "向量XY",    #"Vector2",
    4: "向量XYZ",   #"Vector3"
})

ModifierType = DefEnum("ModifierType", {
    1: "钳制",    # "Clamp",
    2: "取反",    # "Negate",
    3: "死区",    # "Deadzone",
    4: "缩放"     # "Scalar"
})

@sunshine_property_object
class ModifierMeta(PropertyListObject):
    PROPERTIES = {
        "type": PEnum(text="类型", enumType="ModifierType"),
        "clamp": PArray(text="钳制", func= lambda obj: { 'visible': obj.type == 1}, childAttribute=PDict(children={
            "min": PFloat(text="最小值", default=0),
            "max": PFloat(text="最大值", default=1)
        })),
        "negate": PArray(text="取反", func= lambda obj: { 'visible': obj.type == 2}, childAttribute=PBool()),
        "deadzone": PArray(text="死区", func= lambda obj: { 'visible': obj.type == 3}, childAttribute=PFloat(text="半径")),
        "scalar": PArray(text="缩放", func= lambda obj: { 'visible': obj.type == 4}, childAttribute=PFloat())
    }

@sunshine_class_meta
class ActionPartMeta(PartBaseMeta):
    CLASS_NAME = "ActionPart"
    ObjectArrayDef = {
    	"modifiers": ModifierMeta,
    }
    PROPERTIES = {
        #   "int1": PInt(text="整数1", sort=1, default=1, tip="这是个整数", group="分组1"),
        #   "float1": PFloat(text="浮点数1", sort=3, default=1.1),
        #   "bool1": PBool(text="Bool1", sort=5, default=False),
        #   "str2": PStr(text="字符串2", sort=8, default="default"),
        #   "enum1": PEnum(text="枚举1", sort=9, enumType="IntOption"),
        #   "vector2": PVector2(text="二维向量", sort=11),
        #   "color2": PColor(text="颜色2", sort=17, format="#RRGGBB"),
        #   "array2": PArray(text="整数数组", sort=19, childAttribute=PInt()),
        #   "dict2": PDict(text="字典2", sort=21, removable=True, addable=True, children={
        #      "key1": PInt(),
        #      "key2": PStr(),
        #   }),
        "action": PStr(text="动作", sort=90, default=""),
        "allowServer": PBool(text="服务器监听", sort=91, default=True),
        "allowClient": PBool(text="客户端监听", sort=92, default=True),
        "valueType": PEnum(text="值类型", sort=93, enumType="ValueType"),
        "modifiers": PObjectArray(text="修饰器", sort=94, itemCreator=ModifierMeta)
    }
