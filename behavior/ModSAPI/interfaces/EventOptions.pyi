# -*- coding: utf-8 -*-
from typing import TypedDict


class ScriptEventMessageFilterOptions(TypedDict):
    """
    Contains additional options for registering a script event event callback.
    """

    namespaces: list[str]
    """Optional list of namespaces to filter inbound script event messages."""
