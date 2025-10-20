# -*- coding: utf-8 -*-
# from typing import List, Dict, Union


class PlayAnimationOptions(object):
    """
    Contains additional options for how an animation is played.    
    """

    def __init__(self, data):
        self.blendOutTime = data['blendOutTime'] if 'blendOutTime' in data else 0
        """Amount of time to fade out after an animation stops."""
        self.controller = data['controller'] if 'controller' in data else ""
        """Specifies a controller to use that has been defined on the entity."""
        self.nextState = data['nextState'] if 'nextState' in data else ""
        """Specifies the state to transition to."""
        self.players = data['players'] if 'players' in data else []
        """A list of players the animation will be visible to."""
        self.stopExpression = data['stopExpression'] if 'stopExpression' in data else ""
        """Specifies a Molang expression for when this animation should complete."""
