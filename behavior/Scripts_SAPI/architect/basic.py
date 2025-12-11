import mod.client.extraClientApi as clientApi
import mod.server.extraServerApi as serverApi

def isServer():
    return clientApi.GetLocalPlayerId() == '-1'

def getComponentCls():
    if isServer():
        return serverApi.GetComponentCls()
    else:
        return clientApi.GetComponentCls()

def getGoalCls():
    return serverApi.GetCustomGoalCls()

def serverTick():
    return serverApi.GetServerTickTime()

compServer = serverApi.GetEngineCompFactory()
compClient = clientApi.GetEngineCompFactory()