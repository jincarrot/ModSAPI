from typing import TypedDict
from ...interfaces.Vector import Vector3

class RGB(TypedDict):
    red: float
    green: float
    blue: float

class RGBA(TypedDict):
    red: float
    green: float
    blue: float
    alpha: float

class MolangVariableMap:
    """Contains a set of additional variable values for further defining how rendering and animations function."""
    
    def setColorRGB(self, variableName: str, color: RGB):
        """Adds the following variables to Molang:

        <variable_name>.r - Red color value [0-1]

        <variable_name>.g - Green color value [0-1]

        <variable_name>.b - Blue color value [0-1]"""

    def setColorRGBA(self, variableName: str, color: RGBA):
        """Adds the following variables to Molang:

        <variable_name>.r - Red color value [0-1]

        <variable_name>.g - Green color value [0-1]

        <variable_name>.b - Blue color value [0-1]

        <variable_name>.a - Alpha value [0-1]"""

    def setFloat(self, variableName: str, value: float):
        """Adds a float variable to Molang."""
        self.__variables[variableName] = value

    def setSpeedAndDirection(self, variableName: str, speed: float, direction: Vector3):
        """Adds the following variables to Molang:

        <variable_name>.speed - Speed value

        <variable_name>.direction - Direction value (in degrees)"""

    def setVector3(self, variableName: str, vector: Vector3):
        """Adds the following variables to Molang:

        <variable_name>.x - X value

        <variable_name>.y - Y value

        <variable_name>.z - Z value"""
