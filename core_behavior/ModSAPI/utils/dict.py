
def update(a, b):
    # type: (dict, dict) -> dict
    ori = a.copy()
    value = b.copy()
    for key in value:
        if isinstance(ori.get(key), dict):
            ori[key] = update(ori[key], value[key]) if key in value else ori[key]
        elif isinstance(ori.get(key), list):
            ori[key] = (ori[key] + value[key]) if key in value else ori[key]
        else:
            ori[key] = value[key] if key in value else ori[key]
    return ori