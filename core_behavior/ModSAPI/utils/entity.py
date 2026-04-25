from ..interfaces.EntityOptions import EntityQueryOptions
import random

def getEntityFilterBySelector(selector, entity=None):
        # type: (str, any) -> EntityQueryOptions
        """Returns entities that match the given selector."""
        data = {} # type: EntityQueryOptions
        selectorType = selector[1]
        if selectorType == 'p':
            data['type'] = 'minecraft:player'
            data['closest'] = 1
        elif selectorType == 'a':
            data['type'] = 'minecraft:player'
        elif selectorType == 'r':
            data['location'] = {"x": random.randint(-2147483648, 2147483647), "y": random.randint(-2147483648, 2147483647), "z": random.randint(-2147483648, 2147483647)}
            data['closest'] = 1
        elif selectorType == 's':
            data['location'] = entity.location if entity else {"x": 0, "y": 0, "z": 0}
            data['closest'] = 1
        # Process selector arguments
        selectorArgs = selector[3:-2].split(',')
        scoreArg = ""
        for arg in selectorArgs:
            key, value = arg.split('=')
            if key == 'type':
                if value[0] == "!":
                    if 'exludeTypes' not in data:
                        data['excludeTypes'] = []
                    data['excludeTypes'].append(value[1:])
                elif not data.get("type"):
                    data['type'] = value
            elif key == 'name':
                if value[0] == "!":
                    if 'excludeNames' not in data:
                        data['excludeNames'] = []
                    data['excludeNames'].append(value[1:])
                else:
                    data['name'] = value
            elif key == 'tag':
                if value[0] == "!":
                    if 'excludeTags' not in data:
                        data['excludeTags'] = []
                    data['excludeTags'].append(value[1:])
                elif 'tags' not in data:
                    data['tags'] = []
                data['tags'].append(value)
            elif key == 'r':
                pass
            elif key == 'scores':
                pass
