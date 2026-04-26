"""客户端"""
from ModSAPI.client.beta import *

def Test(arg):
    print("Client recieved! id: %s, data: %s" % (arg.id, arg.data))
    print(client.localPlayer)

client.afterEvents.serverSendToClient.subscribe("test", Test)
