
class Source:
    """
    Represents a source with a name and a list of requests.

    Attributes:
        name (str): The name of the source.
        requests (list): A list of dictionaries representing the requests. Each dictionary has 'id' and 'value' keys.
    """

    def __init__(self, name, requests):
        self.name = name
        self.requests = [{'id': request_id, 'value': request_value} for request_id, request_value in requests]

    def total_outflow(self):
        total = 0
        for request in self.requests:
            total += request['value']
        return total

    def outflow_by_name(self, request_name):
        for request in self.requests:
            if request['id'] == request_name:
                return request['value']
        return 0