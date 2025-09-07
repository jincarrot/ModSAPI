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

