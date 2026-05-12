import mod.client.extraClientApi as clientApi

class ScreenNode(clientApi.GetScreenNodeCls()):
    
    def __init__(self, namespace, name, params):
        ScreenNode.__init__(self, namespace, name, params)

class UI:
    """Base class of custom UI."""

    def __init__(self, data):
        identifier = data['identifier']
        self.__uiDef = data['uiDef']
        if ":" not in identifier:
            identifier = "modsapi:" + identifier
        self.__namespace = identifier.split(":")[0]
        self.__name = identifier.split(":")[1]
        clientApi.RegisterUI(self.__namespace, self.__name, "%s.%s" % (self.__class__.__module__, "ScreenNode"), self.__uiDef)

    @staticmethod
    def create(identifier, uiDef):
        # type: (str, str) -> UI
        """Create a customUI object."""
        return UI({"identifier": identifier, "uiDef": uiDef})
    
