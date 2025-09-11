# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi
import random

class ActionFormData(object):
    """Builds a simple player form with buttons that let the player take action."""
    import Entity as en
    import FormResponse as fr

    def __init__(self):
        self.__title = ""
        self.__body = ""
        self.__button = []

    def title(self, titleText):
        # type: (str) -> ActionFormData
        """This builder method sets the title for the modal dialog."""
        self.__title = titleText
        return self
    
    def body(self, bodyText):
        # type: (str) -> ActionFormData
        """Method that sets the body text for the modal form."""
        self.__body = bodyText
        return self
    
    def button(self, text, icon=None):
        # type: (str, str) -> None
        """Adds a button to this form with an icon from a resource pack."""
        self.__button.append([text, icon])
        return self
    
    def show(self, player):
        # type: (en.Player) -> fr.Promise
        """Creates and shows this modal popup form. Returns asynchronously when the player confirms or cancels the dialog."""
        id = random.randint(0, 32767)
        serverApi.GetSystem("SAPI", "world").NotifyToClient(player.id, "showActionForm", {"formId": id, "title": self.__title, "body": self.__body, "button": self.__button})
        return self.fr.Promise(id)

class ModalFormData(object):
    """Used to create a fully customizable pop-up form for a player."""
    import Entity as en
    import FormResponse as fr

    def __init__(self):
        self.__title = ""
        self.__elements = []

    def title(self, titleText):
        # type: (str) -> ModalFormData
        """This builder method sets the title for the modal dialog."""
        self.__title = titleText
        return self
    
    def toggle(self, label, defaultValue=False):
        # type: (str, bool) -> ModalFormData
        """Adds a toggle checkbox button to the form."""
        data = {
            "type": "toggle",
            "label": label
        }
        self.__elements.append(data)
        return self
    
    def title(self, titleText):
        # type: (str) -> None
        """This builder method sets the title for the modal dialog."""
        self.__title = titleText
        return self
    
    def textField(self, label, placeholderText, defaultValue=""):
        # type: (str, str, str) -> ModalFormData
        """Adds a textbox to the form."""
        data = {
            "type": "input",
            "label": label
        }
        self.__elements.append(data)
        return self
    
    def slider(self, label, mininumValue, maxinumValue, valueStep, defaultValue=0):
        # type: (str, int, int, int, int) -> ModalFormData
        """Adds a numeric slider to the form."""
        data = {
            "type": "step_slider",
            "label": label
        }
        self.__elements.append(data)
        return self
    
    def show(self, player):
        # type: (en.Player) -> fr.Promise
        """Creates and shows this modal popup form. Returns asynchronously when the player confirms or cancels the dialog."""
        id = random.randint(0, 32767)
        serverApi.GetSystem("SAPI", "world").NotifyToClient(player.id, "showModalForm", {"formId": id, "title": self.__title, "elements": self.__elements})
        return self.fr.Promise(id)
