class Attr:
    @property
    def value(self):
        # type: () -> any
        """
        获取属性值 (如label, size, color等的值)
        """
        pass

    @value.setter
    def value(self, value):
        pass

    @property
    def name(self):
        # type: () -> str
        """
        获取属性名 (如'label', 'size', 'color'等)
        """
        pass

class Node:
    def on(self, event, callback):
        # type: (str, function) -> None
        """
        监听事件
        """
        pass

    def off(self, event, callback):
        # type: (str, function) -> None
        """
        移除事件监听器
        """
        pass

    def trigger(self, event, args):
        # type: (str, dict) -> None
        """
        手动触发事件
        """
        pass

    @property
    def attributes(self):
        # type: () -> list[Attr]
        """
        获取所有属性
        """
        pass

    def getAttr(self, name):
        # type: (str) -> Attr
        """
        获取指定属性
        """
        pass

class ParentNode(Node):
    @property
    def children(self):
        # type: () -> list[ChildNode]
        """
        获取所有子节点
        """
        pass

    @property
    def first(self):
        # type: () -> ChildNode
        """
        获取第一个子节点
        """
        pass

    @property
    def last(self):
        # type: () -> ChildNode
        """
        获取最后一个子节点
        """
        pass

    def insertAfter(self, node, target):
        # type: (ChildNode, ChildNode) -> ChildNode
        """
        在目标节点之后插入节点
        返回新插入的节点
        """
        pass

    def insertBefore(self, node, target):
        # type: (ChildNode, ChildNode) -> ChildNode
        """
        在目标节点之前插入节点
        返回新插入的节点
        """
        pass

    def appendChild(self, node):
        # type: (ChildNode) -> ChildNode
        """
        在末尾添加子节点
        返回被插入的元素
        """
        pass

    def removeChild(self, node):
        # type: (ChildNode) -> ChildNode
        """
        移除子节点
        返回被移除的节点
        """
        pass

    def replaceChild(self, to, target):
        # type: (ChildNode, ChildNode) -> ChildNode
        """
        替换子节点
        返回被替换的节点
        """
        pass

class ChildNode(Node):
    @property
    def parent(self):
        # type: () -> ParentNode
        """
        获取父节点
        """
        pass

    def before(self, node):
        # type: (ChildNode) -> ChildNode
        """
        在当前节点之前插入节点
        返回新插入的节点
        """
        pass

    def after(self, node):
        # type: (ChildNode) -> ChildNode
        """
        在当前节点之后插入节点
        返回新插入的节点
        """
        pass

    def replaceWith(self, node):
        # type: (ChildNode) -> ChildNode
        """
        替换当前节点
        返回被替换的节点
        """
        pass

    def remove(self):
        # type: () -> None
        """
        移除当前节点
        """
        pass

class Widget(ParentNode, ChildNode):

    def getNodeByName(self, name):
        # type: (str) -> Node
        """
        获取指定名称的节点
        """
        pass

    def getNodesByType(self, type):
        # type: (str) -> list[Node]
        """
        获取指定类型的节点
        """
        pass

    def createNode(self, type, name):
        # type: (str, str) -> Node
        """
        创建节点
        """
        pass


"""
Node是接口不需要实现, 只需要实现 Widget 就行
"""