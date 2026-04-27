# Hello World Upgrade

# 目标：在任意玩家发送"Hello"消息时，向玩家输出 "World"
# 尝试初步使用事件，与游戏交互
from ..ModSAPI.server.beta import * # 导入ModSAPI-server模块

def onChatSend(arg):
    # type: (ChatSendAfterEvent) -> None
    """定义函数，函数名任意，第7行没有实际功能，只是为了方便编写代码。"""
    if arg.message == "Hello": # 判断玩家发送的消息是否为"Hello"
        arg.sender.sendMessage("World") # 向玩家发送消息"World"

world.afterEvents.chatSend.subscribe(onChatSend) # 注册监听
