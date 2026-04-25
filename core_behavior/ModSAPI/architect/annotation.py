class AnnotationHelper:
    @staticmethod
    def addAnnotation(target, key, value):
        if not hasattr(target, '_annotations'):
            target._annotations = {}
        target._annotations[key] = value

    @staticmethod
    def getAnnotation(target, key):
        if hasattr(target, '_annotations'):
            return target._annotations.get(key)
        return None
    
    @staticmethod
    def findAnnotatedMethods(target, key):
        methods = []
        for attr_name in dir(target):
            attr = getattr(target, attr_name)
            if callable(attr) and hasattr(attr, '_annotations'):
                if key in attr._annotations:
                    methods.append(attr)
        return methods
    
    @staticmethod
    def findAnnotatedClasses(target, key):
        classes = []
        for attr_name in dir(target):
            attr = getattr(target, attr_name)
            if isinstance(attr, type) and hasattr(attr, '_annotations'):
                if key in attr._annotations:
                    classes.append(attr)
        return classes
    
    @staticmethod
    def findAnnotatedAttributes(target, key):
        attributes = []
        for attr_name in dir(target):
            attr = getattr(target, attr_name)
            if not callable(attr) and hasattr(attr, '_annotations'):
                if key in attr._annotations:
                    attributes.append(attr)
        return attributes