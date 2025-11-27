class Node:
    def on(self, event, callback):
        pass

    def off(self, event, callback):
        pass

    def trigger(self, event, args):
        pass

    def attributes(self):
        pass

    def getAttr(self, name):
        pass

class ParentNode(Node):
    @property
    def children(self):
        pass

    @property
    def first(self):
        pass

    @property
    def last(self):
        pass

    def insertAfter(self, node, target):
        pass

    def insertBefore(self, node, target):
        pass

    def appendChild(self, node):
        pass

    def removeChild(self, node):
        pass

    def replaceChild(self, to, target):
        pass

class ChildNode(Node):
    @property
    def parent(self):
        pass

    def before(self, node):
        pass

    def after(self, node):
        pass

    def replaceWith(self, node):
        pass

    def remove(self):
        pass


class Widget(ParentNode):

    def getNodeByName(self, name):
        pass

    def getNodesByType(self, type):
        pass

    def createNode(self, type, name):
        pass