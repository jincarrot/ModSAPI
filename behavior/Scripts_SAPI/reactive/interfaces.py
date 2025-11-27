from ..Classes.UI import *

class CONTROLS:
    IMAGE=Image
    LABEL=Label
    PANEL=Panel
    BUTTON=Button

class Attr:

    def __init__(self, name, control):
        # type: (str, Control) -> None
        self.__control = control
        self.__name = name

    @property
    def value(self):
        # type: () -> any
        """
        获取属性值 (如label, size, color等的值)
        """
        return getattr(self.__control, self.__name)

    @value.setter
    def value(self, value):
        setattr(self.__control, self.__name, value)

    @property
    def name(self):
        # type: () -> str
        """
        获取属性名 (如'label', 'size', 'color'等)
        """
        return self.__name

class Node:
    
    def __init__(self, control):
        # type: (Control) -> None
        self._control = control
        
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
        attrOrMethods = dir(self._control)
        attrs = []
        for propertyName in attrOrMethods:
            if propertyName[0] == '_':
                continue
            if callable(getattr(self._control, propertyName)):
                continue
            attrs.append(propertyName)
        result = []
        for attr in attrs:
            result.append(Attr(attr, self._control))
        return result

    def getAttr(self, name):
        # type: (str) -> Attr
        """
        获取指定属性
        """
        return Attr(name, self._control)

class ParentNode(Node):

    def __init__(self, control):
        # type: (Control) -> None
        self._control = control

    @property
    def children(self):
        # type: () -> list[ChildNode]
        """
        获取所有子节点
        """
        childs = self._control._controlData.controls
        instances = []
        for i in childs:
            if i.inst:
                instances.append(ChildNode(i.inst))
        return instances

    @property
    def first(self):
        # type: () -> ChildNode
        """
        获取第一个子节点
        """
        return self.children[0]

    @property
    def last(self):
        # type: () -> ChildNode
        """
        获取最后一个子节点
        """
        return self.children[-1]

    def insertAfter(self, node, target):
        # type: (ChildNode, ChildNode) -> ChildNode
        """
        在目标节点之后插入节点
        返回新插入的节点
        """
        new = self._control.addControl(target._control)
        controls = self._control._controlData.controls
        ori = len(controls)
        for i in range(len(controls)):
            if controls[i].inst == node._control:
                controls.insert(i + 1, controls[-1])
                break
        controls.pop()
        if len(controls) == ori:
            print("Node doesn't exist!")
            return
        return ChildNode(new)

    def insertBefore(self, node, target):
        # type: (ChildNode, ChildNode) -> ChildNode
        """
        在目标节点之前插入节点
        返回新插入的节点
        """
        new = self._control.addControl(target._control)
        controls = self._control._controlData.controls
        ori = len(controls)
        for i in range(len(controls)):
            if controls[i].inst == node._control:
                controls.insert(i, controls[-1])
                break
        controls.pop()
        if len(controls) == ori:
            print("Node doesn't exist!")
            return
        return ChildNode(new)

    def appendChild(self, node):
        # type: (ChildNode) -> ChildNode
        """
        在末尾添加子节点
        返回被插入的元素
        """
        new = self._control.addControl(node._control)
        return ChildNode(new)

    def removeChild(self, node):
        # type: (ChildNode) -> ChildNode
        """
        移除子节点
        返回被移除的节点
        """
        controls = self._control._controlData.controls
        ori = len(controls)
        controls.remove(node._control._controlData)
        if len(controls) == ori:
            print("Node doesn't exist!")
            return
        return node

    def replaceChild(self, to, target):
        # type: (ChildNode, ChildNode) -> ChildNode
        """
        替换子节点
        返回被替换的节点
        """
        self._control.addControl(target._control)
        controls = self._control._controlData.controls
        ori = None
        for i in range(len(controls)):
            if controls[i].inst == to._control:
                ori = controls[i].inst
                controls[i] = controls[-1]
                break
        controls.pop()
        return ChildNode(ori)

class ChildNode(Node):
    
    def __init__(self, control):
        # type: (Control) -> None
        self._control = control

    @property
    def parent(self):
        # type: () -> ParentNode
        """
        获取父节点
        """
        return ParentNode(self._control.parent) if self._control.parent else None

    def before(self, node):
        # type: (ChildNode) -> ChildNode
        """
        在当前节点之前插入节点
        返回新插入的节点
        """
        self.parent.insertBefore(self, node)

    def after(self, node):
        # type: (ChildNode) -> ChildNode
        """
        在当前节点之后插入节点
        返回新插入的节点
        """
        self.parent.insertAfter(self, node)

    def replaceWith(self, node):
        # type: (ChildNode) -> ChildNode
        """
        替换当前节点
        返回被替换的节点
        """
        self.parent.replaceChild(node, self)

    def remove(self):
        # type: () -> None
        """
        移除当前节点
        """
        self.parent.removeChild(self)

class Widget(ParentNode, ChildNode):

    def __init__(self, control):
        # type: (Control) -> None
        self._control = control

    def getNodeByName(self, name):
        # type: (str) -> Node
        """
        获取指定名称的节点
        """
        def getControl(current):
            # type: (Control) -> Node
            if current.name == name:
                return Node(self._control)
            else:
                for c in current._controlData.controls:
                    getControl(c.inst)
                return None
        return getControl(self._control)

    def getNodesByType(self, type):
        # type: (str) -> list[Node]
        """
        获取指定类型的节点
        """
        nodes = []
        def getControl(current):
            # type: (Control) -> Node
            if current.__class__.__name__.lower() == type:
                nodes.append(Node(self._control))
            else:
                for c in current._controlData.controls:
                    getControl(c.inst)
        getControl(self._control)
        return nodes

    def createNode(self, type, name):
        # type: (str, str) -> Node
        """
        创建节点
        """
        type = type.upper()
        control = getattr(CONTROLS, type)(name=name)
        return Node(control)


"""
Node是接口不需要实现, 只需要实现 Widget 就行
"""