from water_manage.request import Request

class Allocator:
    """The Allocator is used to allocate multiple demands of a finite and limited source amount.
    
        Attributes
        ----------
        supply : rate Quantity
            The supply that is being allocated
        requests : list of Request objects
            Individual requests being made on the source with each having a name associated with
            the requested amount along with a priority number
        deliveries : dict
            The dictionary is a list of named deliveries
            Note that curtailment of request is shared among all demands proportional to it's demand.

        Methods
        -------
        update() : calculates the delivery to each request
        add_request() : add new request to the list
        
    """
    def __init__(self, supply, requests):
        """Initialize the amount and a list of requests with associated priorities for allocation"""
        self.supply = supply
        self._units = supply.units
        self.requests = sorted(requests, key=lambda x: x.priority)
        self.num_requests = len(requests)
        self.remain_amount = self.supply
        self.deliveries = {}
        
    def add_request(self, name, amount, priority=1):
        new_request = Request(name, amount, priority)
        self.requests.append(new_request)
        self.num_requests = len(self.requests)
        self.requests = sorted(self.requests, key=lambda x: x.priority)
        
    def get_request(self, name):
        for i in range(self.num_requests):
            if name == self.requests[i].name:
                request = self.requests[i]
                break
        return request
    
    def update(self):
        """Iterate over each demand and allocate supply.
            
            Starting with the highest priority request, remove the requested amount from
            the supply and continue down the list by providing the remainder supply until
            remainder is zero.
            
            If 1 or more requests have equal priority, then add all these up and allocate
            as one entity then divide amount supplied in proportion to each request amount.
            
            Parameters
            ----------
            
            Returns
            -------
            None
        """
        i = 0
        while True:
            # Iterate over the requests until the end is hit.
            if i == self.num_requests:
                # After we iterate over all requests, add just one more for remainder
                self.deliveries['remainder'] = self.remain_amount
                break
                
            first_index = i
            # Group all requests with equal priority
            request_group = [self.requests[i]]

            while True:
                # Find all subsequent requests that have the same priority
                # The group of requests with the same priority are called a "request_group"
                # Start with the first in the request_group
                if i == self.num_requests - 1:
                    # We are looking at the last request in the list
                    i += 1
                    break
                this_request = self.requests[i]
                next_request = self.requests[i + 1]
                if this_request.priority == next_request.priority:
                    # append to request_group
                    request_group.append(self.requests[i + 1])
                    # cluster_request_amount += self.requests[cluster_index + 1].amount
                    i += 1
                else:
                    # If the end of the list is reached, stop iterating over list of requests
                    i += 1
                    break
            self.allocate(request_group, first_index)
            
    def allocate(self, requests, index=0):
        """Perform allocation of the supply from all requests of the same priority.
        
            Parameters
            ----------
            requests : list of requests
                Contains 1 or more requests of equal priority.
            index : int
                The index of the first request in the group.
        """
        
        request_amount = sum(request.amount for request in requests)
        request_count = len(requests)
        if self.remain_amount >= request_amount:
            for i in range(request_count):
                amount = self.requests[index + i].amount
                name = self.requests[index + i].name
                self.deliveries[name] = amount
                self.remain_amount -= amount
        else:
            shortage = request_amount - self.remain_amount
            for i in range(request_count):
                curtailment = shortage * self.requests[index + i].amount / request_amount
                amount = self.requests[index + i].amount - curtailment
                name = self.requests[index + i].name
                self.deliveries[name] = amount
            self.remain_amount = 0.0 * self._units
