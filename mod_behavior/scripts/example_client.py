"""客户端"""
from ModSAPI.client.beta import *

def Test(arg):
    print("Client recieved! id: %s, data: %s" % (arg.id, arg.data))

client.afterEvents.serverEventReceive.subscribe("test", Test)
