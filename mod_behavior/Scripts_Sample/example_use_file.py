"""接近SAPI的使用方式，需要在config.py中定义入口文件名"""
from ModSAPI.server.beta import *
from ModSAPI.serverui.beta import *

def onChatSend(arg):
    # type: (ChatSendAfterEvent) -> None
    print("ChatSend event in 'example_use_file', sender: %s" % str(arg.sender))
    print(arg.sender.dimension.spawnItem(ItemStack("minecraft:diamond", 1), arg.sender.location))
    print(world.getAllPlayers())
    print(arg.sender.dimension.runCommand("say t"))

world.afterEvents.chatSend.subscribe(onChatSend) # 监听事件

def Test(arg):
    # type: (EntityHurtAfterEvent) -> None
    if arg.damageSource.damagingEntity.typeId != "minecraft:player":
        return
    system.sendToClient(arg.damageSource.damagingEntity, "test", 111)
    visible = Observable.create(True)
    text = Observable.create("title", {"clientWritable": True})
    form = CustomForm.create(arg.damageSource.damagingEntity, "测试")
    def onClick():
        visible.setData(not visible.getData())
    form.button("测试", onClick)
    form.textField(text, text, {"visible": visible})
    form.show()

world.afterEvents.entityHurt.subscribe(Test)