# -*- coding: utf-8 -*-
from typing import TypedDict
from Vector import Vector3

class ParticleBindEntityOptions(TypedDict):
    bone: str
    offset: Vector3
    rotate: Vector3
