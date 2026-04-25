
class ConstMeta(type):
    def __setattr__(cls, name, value):
        raise AttributeError("Constant '{0}' cannot be reassigned".format(name))