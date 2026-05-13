# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi

class FormResponse(object):
    """Base type for a form response."""
    @property
    def canceled(self):
        """If true, the form was canceled by the player (e.g., they selected the pop-up X close button)."""

class ActionFormResponse(FormResponse):
    """Returns data about the player results from a modal action form."""

    @property
    def selection(self):
        # type: () -> int
        """Returns the index of the button that was pushed."""

class ModalFormResponse(FormResponse):
    """Returns data about the player results from a modal action form."""
    @property
    def values(self):
        # type: () -> list[int | bool | str]
        """Returns the values of the form fields."""
