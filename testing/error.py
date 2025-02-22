
class Error(Exception):
    """Base class for exceptions found in Aegis.
    """
    
    pass


class WrongUnits(Error):
    def __init__(self, m):
        self.message = m
    
    pass


class NodeNotFound(Error):
    """Node is not found when searching a list
    """
    pass


class NodeAlreadyExists(Error):
    """Node already exists and you are looking to create a
    unique one.
    """
    
    pass


def exception_handler(exception_type, exception, traceback):
    # All your trace are belong to us!
    # your format
    print("%s: %s" % (exception_type.__name__, exception))