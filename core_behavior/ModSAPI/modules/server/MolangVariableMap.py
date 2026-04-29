
from ...interfaces.Vector import Vector3

class RGB:
    pass

class RGBA:
    pass

class MolangVariableMap:
    """Contains a set of additional variable values for further defining how rendering and animations function."""
    def __init__(self):
        self.__variables = {}
    
    def setColorRGB(self, variableName, color):
        """Adds the following variables to Molang:

        <variable_name>.r - Red color value [0-1]

        <variable_name>.g - Green color value [0-1]

        <variable_name>.b - Blue color value [0-1]"""
        color = {"type": "rgb", "value": color}
        self.__variables[variableName] = color

    def setColorRGBA(self, variableName, color):
        """Adds the following variables to Molang:

        <variable_name>.r - Red color value [0-1]

        <variable_name>.g - Green color value [0-1]

        <variable_name>.b - Blue color value [0-1]

        <variable_name>.a - Alpha value [0-1]"""
        color = {"type": "rgba", "value": color}
        self.__variables[variableName] = color

    def setFloat(self, variableName, value):
        """Adds a float variable to Molang."""
        value = {"type": "float", "value": value}
        self.__variables[variableName] = value

    def setSpeedAndDirection(self, variableName, speed, direction):
        """Adds the following variables to Molang:

        <variable_name>.speed - Speed value

        <variable_name>.direction - Direction value (in degrees)"""
        direction = Vector3(direction)
        self.__variables[variableName] = {"type": "speed_and_direction", "value": {"speed": speed, "direction": direction.getTuple()}}

    def setVector3(self, variableName, vector):
        """Adds the following variables to Molang:

        <variable_name>.x - X value

        <variable_name>.y - Y value

        <variable_name>.z - Z value"""
        vector = Vector3(vector)
        self.__variables[variableName] = {"type": "vector3", "value":  vector.getTuple()}
    
    def getData(self):
        """Gets the data of this MolangVariableMap."""
        return self.__variables
