import inputs.constants as const
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
        outflows : list of rate Quantities
            The resulting deliveries from the source of each demand
            Note that curtailment of request is shared among all demands proportional to it's demand.
        
        Methods
        -------
        outflows() : calculates the outflow for each request
        
    """
    def __init__(self, supply, requests):
        """Initialize the amount and a list of requests with associated priorities for allocation"""
        self.supply = supply
        self._units = supply.units
        self.requests = sorted(requests, key=lambda x: x.priority)
        self.remainder = 0 * self._units
        self.num_requests = len(requests)
        self.outflows = [0 * self._units] * (self.num_requests + 1)
        self.remain_amount = self.supply
        self.allocated = [False] * self.num_requests
        self.deliveries = {}
    
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
            outflows : list of tuples (name, amount)
        """
        i = 0
        while True:
            # Iterate over the requests until the end is hit.
            
            if i == self.num_requests:
                # self.allocate(cluster, first_index)
                # self.outflows[i+1] = self.remain_amount
                self.deliveries['remainder'] = self.remain_amount
                break
                
            cluster_index = i
            first_index = cluster_index
            cluster = [self.requests[i]]

            while True:
                # Find all subsequent requests from the current one that have the same priority
                # The group of requests with the same priority are called a "cluster"
                # start with the first in the cluster
                if cluster_index == self.num_requests - 1:
                    # We are looking at the last request in the list
                    cluster_index += 1
                    break
                this_request = self.requests[cluster_index]
                next_request = self.requests[cluster_index + 1]
                if this_request.priority == next_request.priority:
                    # append to cluster
                    cluster.append(self.requests[cluster_index + 1])
                    # cluster_request_amount += self.requests[cluster_index + 1].amount
                    cluster_index += 1
                else:
                    # If the end of the list is reached, stop iterating over list of requests
                    cluster_index += 1
                    break
            i = cluster_index
            self.allocate(cluster, first_index)
            
    def allocate(self, requests, index=0):
        request_amount = sum(request.amount for request in requests)
        request_count = len(requests)
        if self.remain_amount >= request_amount:
            for i in range(request_count):
                amount = self.requests[index + i].amount
                self.outflows[index + i] = amount
                name = self.requests[index + i].name
                self.deliveries[name] = amount
                self.remain_amount -= amount
        else:
            shortage = request_amount - self.remain_amount
            for i in range(request_count):
                curtailment = shortage * self.requests[index + i].amount / request_amount
                amount = self.requests[index + i].amount - curtailment
                self.outflows[index + i] = amount
                name = self.requests[index + i].name
                self.deliveries[name] = amount
            self.remain_amount = 0.0 * self._units
