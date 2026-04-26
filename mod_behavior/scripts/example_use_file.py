"""接近SAPI的使用方式，需要在config.py中定义入口文件名"""
from ModSAPI.server.beta import *

def onChatSend(arg):
    # type: (ChatSendAfterEvent) -> None
    print("ChatSend event in 'example_use_file', sender: %s" % str(arg.sender))
    system.sendToClient(arg.sender, "test", 111)

world.afterEvents.chatSend.subscribe(onChatSend) # 监听事件