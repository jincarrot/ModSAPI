"""接近SAPI的使用方式，需要在config.py中定义入口文件名"""
from ModSAPI.server.beta import *
from ModSAPI.serverui.beta import *

def onChatSend(arg):
    # type: (ChatSendAfterEvent) -> None
    form = ModalFormData()
    form.title("测试")
    form.slider("滑动条", 0, 10, 1)
    form.textField("222", "???")
    form.toggle("开关")
    form.dropdown("下拉框", ["选项1", "选项2", "选项3"])
    form.show(arg.sender).then(lambda res: arg.sender.sendMessage(str(res)))

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