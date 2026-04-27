# Upgrade - SBTI
# 高难度

# 目标：使用表单，让玩家回答问题，得到他的“SBTI”（一种搞怪向人格类型）
# 当玩家在聊天框输入SBTI时，弹出表单。
# 使用表单接口（DDUI），制作更加复杂的功能。
from ..ModSAPI.server.beta import * # 导入ModSAPI-server模块
from ..ModSAPI.serverui.beta import * # 导入ModSAPI-serverui模块

QUESTIONS = [
    {
        "q": "你更喜欢哪种活动？",
        "s": [
            "和朋友们一起聚会",
            "独自在家打游戏",
            "独自旅行",
            "网上冲浪"
        ]
    },
    {
        "q": "你更喜欢哪种工作环境？",
        "s": [
            "安静的",
            "热闹的"
        ]
    }
]

def createForm(player):
    form = CustomForm.create(player, "SBTI测试") # 创建一个自定义表单，参数为表单标题
    # DDUI支持动态创建控件，但无法动态删除，因此我们使用隐藏控件功能来实现翻页效果。
    currentPage = Observable.create(0) # 当前页数

    # page0
    pages = [Observable.create(True), Observable.create(False)] # 创建动态变量，控制页面是否显示。
    answers = {} # 保存玩家的答案
    form.label("欢迎来到SBTI测试！", {"visible": pages[0]}) # 添加文本
    form.spacer({"visible": pages[0]}) # 添加分割线
    form.label("只需要几个简单的问题，即可得到您的人格类型！", {"visible": pages[0]})
    form.divider({"visible": pages[0]})
    def onStart():
        # 当点击开始测试时执行
        currentPage.setData(1)
    form.button("开始测试", onStart, {"visible": pages[0]}) # 添加按钮，点击时执行onStart函数

    # page1
    name = Observable.create("", {"clientWritable": True}) # 创建动态变量，保存玩家输入的名字
    age = Observable.create(0, {"clientWritable": True}) # 创建动态变量，保存玩家输入的年龄
    sex = Observable.create(0, {"clientWritable": True}) # 创建动态变量，保存玩家选择的性别
    form.textField("请输入您的昵称", name, {"visible": pages[1]})
    form.slider("请输入您的年龄", age, 1, 100, {"visible": pages[1]})
    form.dropdown("请选择您的性别", sex, [{"label": "男", "value": 0}, {"label": "女", "value": 1}], {"visible": pages[1]})
    
    # page(questions)
    def onAnswer(selection):
        answers[currentPage.getData() - 2] = selection
        onClickRight()
    question = Observable.create("")
    questionVisible = Observable.create(False)
    selections = [(Observable.create(""), Observable.create(False)) for _ in range(4)]
    form.label(question, {"visible": questionVisible}) \
        .divider({"visible": questionVisible}) \
        .button(selections[0][0], lambda: onAnswer("A"), {"visible": selections[0][1]}) \
        .button(selections[1][0], lambda: onAnswer("B"), {"visible": selections[1][1]}) \
        .button(selections[2][0], lambda: onAnswer("C"), {"visible": selections[2][1]}) \
        .button(selections[3][0], lambda: onAnswer("D"), {"visible": selections[3][1]}) \
        .divider({"visible": questionVisible})
    for _ in QUESTIONS:
        pages.append(None)  # 占位，后续动态创建
    
    # page end
    result = Observable.create("")
    pages.append(Observable.create(False))
    form.label("恭喜你！你的SBTI是——", {"visible": pages[-1]})
    form.divider({"visible": pages[-1]})
    form.button(result, lambda: None, {"visible": pages[-1]})
    # buttons
    left = Observable.create(False)
    right = Observable.create(False)
    submit = Observable.create(False)
    def onChangePage(page):
        left.setData(len(pages) - 1 > page > 1)
        right.setData(page < len(QUESTIONS) + 1)
        submit.setData(page == len(QUESTIONS) + 1)
        if (len(QUESTIONS) + 2) > page > 1:
            question.setData(QUESTIONS[page - 2]["q"])
            questionVisible.setData(True)
            for i in range(4):
                if len(QUESTIONS[page - 2]['s']) > i:
                    s = QUESTIONS[page - 2]['s'][i]
                    selections[i][0].setData(s)
                    selections[i][1].setData(True)
                else:
                    selections[i][1].setData(False)
        else:
            questionVisible.setData(False)
            for i in range(4):
                selections[i][1].setData(False)
        if pages[page]:
            pages[page].setData(True)
        if page < len(pages) - 2:
            pages[page + 1].setData(False) if pages[page + 1] else None
        if page > 0 and page < len(pages) + 1:
            pages[page - 1].setData(False) if pages[page - 1] else None
        temp = "XIAOWA"
        result.setData(temp)
    currentPage.subscribe(onChangePage)
    def onClickLeft():
        currentPage.setData(currentPage.getData() - 1)
    def onClickRight():
        currentPage.setData(currentPage.getData() + 1)
    form.button("上一页", onClickLeft, {"visible": left})
    form.button("下一页", onClickRight, {"visible": right})
    form.button("提交", onClickRight, {"visible": submit})
    form.show()

def onChatSend(arg):
    # type: (ChatSendBeforeEvent) -> None
    if arg.message == "SBTI":
        arg.cancel = True # 取消此次消息的发送
        player = arg.sender
        createForm(player)

world.beforeEvents.chatSend.subscribe(onChatSend)
