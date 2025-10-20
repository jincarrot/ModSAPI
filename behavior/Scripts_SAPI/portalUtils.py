# -*- coding: utf-8 -*-

# common
from types import FunctionType

class ref:
    def __init__(self, value):
        self.value = value

def dimName(dimId):
    if dimId == 0:
        return 'overworld'
    elif dimId == 1:
        return 'nether'
    elif dimId == 2:
        return 'the_end'

    return 'dm{}'.format(dimId)

# common end

# client only
import mod.client.extraClientApi as clientApi
compFactory = clientApi.GetEngineCompFactory()
drawing = compFactory.CreateDrawing(clientApi.GetLevelId())

class BoxRenderer:
    def __init__(self):
        self.errs = []
        self.dones = []

    def fail(self, pos, size=(1,1,1)):
        box = drawing.AddBoxShape(pos, size, (1, 0, 0))
        self.errs.append(box)
        return box

    def done(self, pos, size=(1,1,1)):
        box = drawing.AddBoxShape(pos, size, (0, 1, 1))
        self.dones.append(box)
        return box

    def clearError(self):
        for b in self.errs:
            b.Remove()

    def clearDone(self):
        for b in self.dones:
            b.Remove()

    def clearAll(self):
        self.clearDone()
        self.clearError()

defaultChecker = lambda block: block[0] == 'minecraft:fire' or block[0] == 'minecraft:air'

def __checkGatePathInfo(blockType, pos, checker=defaultChecker):
    # type: (str, tuple[int, int, int], FunctionType) -> None | tuple[tuple[int, int, int], tuple[int, int, int]]
    blockInfo = compFactory.CreateBlockInfo(clientApi.GetLevelId())
    checked = []
    state = ref(0)
    result = ref(None)

    # 矩形区域一定可以用最大和最小坐标表示
    def calcArea():
        (x1, y1, z1) = pos
        (x2, y2, z2) = pos
        for (x, y, z) in checked:
            if x < x1:
                x1 = x
            if y < y1:
                y1 = y
            if z < z1:
                z1 = z
            if x > x2:
                x2 = x
            if y > y2:
                y2 = y
            if z > z2:
                z2 = z

        return ((x1, y1, z1), (x2, y2, z2))
    
    def error():
        state.value = 1
        area = calcArea()
        result.value = area
    
    # dir 为 0 时表示 x 轴方向，1 时表示 z 轴方向
    def checkGateInfo(blockType, pos, last, dir=0):
        block = blockInfo.GetBlock(pos)

        # 多余的一次移动
        if block[0] == blockType:
            return

        if pos in checked:
            area = calcArea()
            state.value = 2
            result.value = area
            return

        if not checker(block):
            state.value = 1

        if state.value > 0:
            return

        checked.append(pos)
        (x, y, z) = pos

        up    = (x, y + 1, z)
        right = (x + 1, y, z) if dir == 0 else (x, y, z + 1)
        left  = (x - 1, y, z) if dir == 0 else (x, y, z - 1)
        down  = (x, y - 1, z)

        upBlock    = blockInfo.GetBlock(up)[0]
        rightBlock = blockInfo.GetBlock(right)[0]
        downBlock  = blockInfo.GetBlock(down)[0]
        leftBlock  = blockInfo.GetBlock(left)[0]
        
        matched = 0
        nextIteration = []

        if upBlock == blockType:
            matched += 1
            if last > -1 and last != 0 and rightBlock != blockType:
                return error()
            nextIteration.append(lambda: checkGateInfo(blockType, left, 0, dir))

        if rightBlock == blockType:
            matched += 1
            if last > -1 and last != 1 and downBlock != blockType:
                return error()
            nextIteration.append(lambda: checkGateInfo(blockType, up, 1, dir))
        
        if downBlock == blockType:
            matched += 1
            if last > -1 and last != 2 and leftBlock != blockType:
                return error()
            nextIteration.append(lambda: checkGateInfo(blockType, right, 2, dir))

        if leftBlock == blockType:
            matched += 1
            if last > -1 and last != 3 and upBlock != blockType:
                return error()
            nextIteration.append(lambda: checkGateInfo(blockType, down, 3, dir))

        #没有任何一边是边缘，说明没有闭合
        if matched == 0 or matched > 2:
            return error()
        
        for it in nextIteration:
            it()
        
    checkGateInfo(blockType, pos, -1)

    if state.value == 2:
        return result.value
    
    checked = []
    state.value = 0
    checkGateInfo(blockType, pos, -1, 1)

    if state.value == 2:
        return result.value
    
    return None

def __getGateBoundingRectFromInsetBorder(blockType, pos, checker=defaultChecker, size=(2, 3)):
    blockInfo = compFactory.CreateBlockInfo(clientApi.GetLevelId())
    area = __checkGatePathInfo(blockType, pos, checker)
    if not area:
        return None
    
    ((x1, y1, z1), (x2, y2, z2)) = area
    size = (x2 - x1 + 1, y2 - y1 + 1, z2 - z1 + 1)
    facingX = size[0] == 1
    area2dRect = (size[2], size[1]) if facingX else (size[0], size[1])

    # 判断尺寸是否大于最小值
    if area2dRect[0] < size[0] or area2dRect[1] < size[1]:
        return None

    # 判断中间方块是否都都能通过 checker 测试
    for i in range(y1, y2):
        if facingX:
            for z in range(z1, z2):
                if not checker(blockInfo.GetBlock((x1, i, z))):
                    return None
        else:
            for x in range(x1, x2):
                if not checker(blockInfo.GetBlock((x, i, z1))):
                    return None

    return area

def __findPointOnGateBorder(blockType, posInset, checker=defaultChecker, maxStep=64):
    blockInfo = compFactory.CreateBlockInfo(clientApi.GetLevelId())
    records = []

    records.append(posInset)

    def innerSpaceIter(pos):
        (x, y, z) = pos

        d = (x, y - 1, z)
        d_ = blockInfo.GetBlock(d)

        yield (d, d_)
        iter = innerSpaceIter(d)
        for (pos, block) in iter:
            yield (pos, block)

    for (pos, block) in innerSpaceIter(posInset):
        if len(records) >= maxStep:
            return None

        if not checker(block):
            if block[0] != blockType:
                return None
            else:
                return records.pop()
        
        records.append(pos)

    return None

def getMatchedAroundPoint(pos, checker=defaultChecker):
    # type: (tuple[int, int, int], FunctionType) -> list[tuple[int, int, int]]
    """
    使用checker检测 pos 及 周围的方块，返回满足 checker 的方块
    """
    blockInfo = compFactory.CreateBlockInfo(clientApi.GetLevelId())

    (x, y, z) = pos

    up = (x, y + 1, z)
    down = (x, y - 1, z)
    right = (x + 1, y, z)
    left = (x - 1, y, z)
    front = (x, y, z + 1)
    back = (x, y, z - 1)

    result = []

    if checker(blockInfo.GetBlock(pos)):
        result.append(pos)

    if checker(blockInfo.GetBlock(up)):
        result.append(up)

    if checker(blockInfo.GetBlock(down)):
        result.append(down)

    if checker(blockInfo.GetBlock(right)):
        result.append(right)
    
    if checker(blockInfo.GetBlock(left)):
        result.append(left)

    if checker(blockInfo.GetBlock(front)):
        result.append(front)

    if checker(blockInfo.GetBlock(back)):
        result.append(back)

    return result

def getBoundingGate(borderBlockType, pos, checker=defaultChecker, size=(2, 3), maxFindStep=64):
    # type: (str, tuple[int, int, int], FunctionType, tuple[int, int], int) -> tuple[tuple[int, int, int], tuple[int, int, int]]
    """
    通过传送门内一个点，获取传送门边界
    """
    possiblePoint = __findPointOnGateBorder(borderBlockType, pos, checker, maxFindStep)
    if not possiblePoint:
        return None

    return __getGateBoundingRectFromInsetBorder(borderBlockType, possiblePoint, checker, size)

def isMatchedRect(rect, checker=defaultChecker):
    # type: (tuple[tuple[int, int, int], tuple[int, int, int]], FunctionType) -> bool
    """
    检查一个区域是否满足 checker
    """
    ((x1, y1, z1), (x2, y2, z2)) = rect
    blockInfo = compFactory.CreateBlockInfo(clientApi.GetLevelId())

    for x in range(x1, x2):
        for y in range(y1, y2):
            for z in range(z1, z2):
                if not checker(blockInfo.GetBlock((x, y, z))):
                    return False

    return True
# client only end

# server only
import mod.server.extraServerApi as serverApi
serverFactory = serverApi.GetEngineCompFactory()
def fillBlocks(space, blockType):
    # type: (tuple[tuple[int,int,int], tuple[int,int,int], int], str) -> bool
    """
    :param space: (fromPos, toPos, dimensionId)
    """
    ((x1, y1, z1), (x2, y2, z2), dim) = space
    command = serverFactory.CreateCommand(serverApi.GetLevelId())
    command.SetCommand('execute in {} run fill {} {} {} {} {} {} {}'.format(
        dimName(dim), x1, y1, z1, x2, y2, z2, blockType
    ))
# server only end

"""
关于函数导出
common:
    - ref
    - dirName

client:
    - class BoxRenderer
    - getBoundingGate
    - isMatchedRect
    - getMatchedAroundPoint (用于破坏传送门框的时候，破坏相关传送门方块)

server:
    - fillBlocks
"""

"""
关于传送门创建/销毁

创建：
    - 客户端检测到传送门方块后检查是否是完整的传送门结构
    - 如果是，发送 portalGateCreate 事件到服务器(包含需要创建的区域信息)
    - 服务器接收到事件后，通过playerId获得dimension创建传送门（fillBlocks），并广播 portalGateCreated 事件到所有客户端

销毁：
    - 客户端检测被破坏的是传送门方块还是传送门门框方块
        - 传送门门框方块
            - 只需要查找六个方向内的传送门方块是否存在（getMatchedAroundPoint）
            - 如果存在，检测传送门方块
        - 传送门方块
            - 是否在已知传送门区域内
                - 如果是，发送 portalGateDestroy 事件到服务器(包含需要销毁的区域信息)
                - 服务器接收到事件后，通过playerId获得dimension销毁传送门（fillBlocks），并广播 portalGateDestroyed 事件到所有客户端

为什么不直接让服务端检测传送门创建/销毁？
    - 传送门检测算法复杂，服务端实现会导致性能问题（稳定的服务端tps远比客户端的low帧重要）
    - 传送门创建/销毁频率较低，客户端检测不会带来太大负担
"""