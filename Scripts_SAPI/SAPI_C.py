# coding=utf-8
import mod.client.extraClientApi as clientApi
import math, time
from Classes.ClientEvents import *
from Classes.Request import *
from scheduler import Scheduler
from minecraft import *

ClientSystem = clientApi.GetClientSystemCls()

CComp = clientApi.GetEngineCompFactory()


class SAPI_C(ClientSystem):
    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        self.__ListenEvent()
        print("SAPI_C loaded")

    def __ListenEvent(self):
        self.ListenForEvent("SAPI", "world", "getData", self, self.getData)
        self.ListenForEvent("SAPI", "world", "sendToast", self, self.sendToast)
        self.ListenForEvent("SAPI", "world", "showActionForm", self, self.showActionForm)
        self.ListenForEvent("SAPI", "world", "showModalForm", self, self.showModalForm)
        self.ListenForEvent("SAPI", "world", "setMusicState", self, self.setMusicState)
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "UiInitFinished", self, self.initUI)
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "OnLocalPlayerStopLoading", self, self.playerSpawn)

    def initUI(self, data):
        clientApi.RegisterUI("server_ui", "ActionForm", "Scripts_SAPI.Classes.Forms.ActionForm", "server_forms.action_form")
        clientApi.RegisterUI("server_ui", "ModalForm", "Scripts_SAPI.Classes.Forms.ModalForm", "server_forms.modal_form")

    def getData(self, data):
        """receive request from server"""
        requestId = data['requestId']
        requestDataName = data['dataName']
        data = None
        if requestDataName == 'clientSystemInfo':
            data = {
                "maxRenderDistance": None,
                "platformType": clientApi.GetPlatform()
            }
        request.update(requestId, data)

    def sendToast(self, data):
        CComp.CreateGame(clientApi.GetLevelId()).SetPopupNotice(data['message'], data['title'])

    def showActionForm(self, data):
        clientApi.PushScreen("server_ui", "ActionForm", data)

    def showModalForm(self, data):
        clientApi.PushScreen("server_ui", "ModalForm", data)

    def playerSpawn(self, data):
        self.NotifyToServer("playerSpawn", data)
    
    def setMusicState(self, data):
        CComp.CreateCustomAudio(clientApi.GetLevelId()).DisableOriginMusic(not data['state'])


def ClientMethod(func):
    """client method"""
    def wrapper(*args, **kwargs):
        global system
        if not system:
            system = getSystem()
        result = func(*args, **kwargs)
        return result
    return wrapper

class ClientP(ClientSystem):

    _frameScheduler = Scheduler()
    _scriptScheduler = Scheduler()

    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        self.__afterEvents = ClientAfterEvents()
        self.__beforeEvents = ClientBeforeEvents()
        self._initScheduler()
        print("SAPI: client loaded")

    @property
    def afterEvents(self):
        return self.__afterEvents
    
    @property
    def beforeEvents(self):
        return self.__beforeEvents
    
    @property
    def camera(self):
        return 1
    
    def _OnScriptTickClient(self):
        self._scriptScheduler.executeSequenceAsync()
    
    def _OnGameRenderTick(self, __data):
        self._frameScheduler.executeSequenceAsync()

    def _initScheduler(self):
        self.ListenForEvent(
            clientApi.GetEngineNamespace(),
            clientApi.GetEngineSystemName(),
            "OnScriptTickClient",
            self,
            self._OnScriptTickClient
        )

        self.ListenForEvent(
            clientApi.GetEngineNamespace(),
            clientApi.GetEngineSystemName(),
            "GameRenderTickEvent",
            self,
            self._OnGameRenderTick
        )

    @staticmethod
    def onUpdate(fn, stage='Update'):
        return ClientP._frameScheduler.addTask(stage, fn)

    @staticmethod
    def onTick(fn, stage='Update'):
        return ClientP._scriptScheduler.addTask(stage, fn)
    
    @staticmethod
    def Timer(fn, ticks=1, interval=False):
        return ClientP._scriptScheduler.runTimer(fn, ticks, interval)
    
    @staticmethod
    def removeTimer(id):
        # type: (int) -> None
        ClientP._scriptScheduler.removeTask('SchedulerTask', id)

    @staticmethod
    def removeTask(stage, id):
        # type: (str, int) -> None
        ClientP._frameScheduler.removeTask(stage, id)


class Client(ServerSystem):
    """
    A class that provides client system.
    """

    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        self.__afterEvents = ClientAfterEvents()
        self.__beforeEvents = ClientBeforeEvents()
        print("ModSAPI: client-loader loaded")

    @property
    def afterEvents(self):
        # request.create()
        pass
