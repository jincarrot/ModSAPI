# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi

def ServerMethod(func):
    def void(*args):
        pass
    def wrapper(*args, **kwargs):
        if not clientApi.GetLocalPlayerId():
            return func(*args, **kwargs)
        else:
            return void(*args, **kwargs)
    return wrapper

def ClientMethod(func):
    def void(*args):
        pass
    def wrapper(*args, **kwargs):
        if clientApi.GetLocalPlayerId():
            return func(*args, **kwargs)
        else:
            return void(*args, **kwargs)
    return wrapper
