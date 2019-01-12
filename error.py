
class Error(Exception):
    """Base class for exceptions found in Aegis.
    """
    
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