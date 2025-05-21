# -*- coding: utf-8 -*-
from Preset.Model.PartBase import PartBase
from Preset.Model.GameObject import registerGenericClass


@registerGenericClass("EnhancedInputMappingPart")
class EnhancedInputMappingPart(PartBase):
    def __init__(self):
        PartBase.__init__(self)
        # 零件名称
        self.name = "输入映射"
        self.action = ""
        self.keys = []
        self.triggers = []
        self.broadcastToServer = True
        
    def Triggers(self):
        return self.triggers

    def Keys(self):
        return self.keys

    def Action(self):
        return self.action

    def BroadcastToServer(self):
        return self.broadcastToServer

    def InitClient(self):
        """
        @description 客户端的零件对象初始化入口
        """
        PartBase.InitClient(self)

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
