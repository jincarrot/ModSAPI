# -*- coding: utf-8 -*-
from Meta.ClassMetaManager import sunshine_class_meta
from Meta.EnumMeta import DefEnum
from Meta.TypeMeta import PBool, PStr, PInt, PCustom, PVector3, PVector3TF, PEnum, PDict, PFloat, PArray, PVector2, PColor, PObjectArray
from Preset.Model import PartBaseMeta
from Preset.Model.PresetDataMeta import PropertyListObject
from Meta.PropertyObject import sunshine_property_object

@sunshine_class_meta
class EnhancedInputPartMeta(PartBaseMeta):
	CLASS_NAME = 'EnhancedInputPart'
	PROPERTIES = {
		'mappingConf': PArray(sort=999, text='映射上下文', childAttribute=PDict(children={
			'contextId': PStr(sort=90, text='上下文id'),
		    'inputMapping': PArray(sort=92, text='输入映射零件名', childAttribute=PStr()),
        })),
	}

