# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi

class FormResponse(object):
    """Base type for a form response."""

    def __init__(self, data):
        self._canceled = data['canceled']

    def __str__(self):
        data = {
            "canceled": self._canceled
        }
        return "<FormResponse> %s" % data

    @property
    def canceled(self):
        """If true, the form was canceled by the player (e.g., they selected the pop-up X close button)."""
        return self._canceled

class Promise(object):
    """Promise"""

    def __init__(self, id):
        self.__id = id

    def then(self, callback):
        serverApi.GetSystem("SAPI", "Base").setFormCallback(self.__id, callback)

class ActionFormResponse(FormResponse):
    """Returns data about the player results from a modal action form."""

    def __init__(self, data):
        FormResponse.__init__(self, data)
        self.__selection = data['buttonId']

    def __str__(self):
        data = {
            "canceled": self._canceled,
            "selection": self.__selection
        }
        return "<ActionFormResponse> %s" % data

    @property
    def selection(self):
        # type: () -> int
        """Returns the index of the button that was pushed."""
        return self.__selection

class ModalFormResponse(FormResponse):
    """Returns data about the player results from a modal action form."""

    def __init__(self, data):
        FormResponse.__init__(self, data)
        self.__values = data['data']

    def __str__(self):
        data = {
            "canceled": self._canceled,
            "values": self.__values
        }
        return "<ModalFormResponse> %s" % data

    @property
    def values(self):
        # type: () -> int
        """Returns the index of the button that was pushed."""
        return self.__values
