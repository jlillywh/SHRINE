# Class for handling names of attributes between classes


class AttrMap(object):
    def __init__(self, name):
        self.name = name
    
    def __get__(self, obj, typ):
        # Read access to obj's attribute.
        if obj is None:
            # access to class -> return descriptor object.
            return self
        return getattr(obj, self.name)
    
    def __set__(self, obj, value):
        return setattr(obj, self.name, value)
    
    def __delete__(self, obj):
        return delattr(obj, self.name)
