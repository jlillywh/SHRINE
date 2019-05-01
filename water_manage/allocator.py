import inputs.constants as const
from water_manage.request import Request


class Allocator:
    """The Allocator is used to allocate multiple demands of a finite and limited source amount.
    
        Attributes
        ----------
        supply : Quantity
            The supply that is being allocated
        requests : list of Request objects
            Individual requests being made on the source with each having a name associated with
            the requested amount along with a priority number
        proportional : bool
            Flag for proportional curtailment if sum demands > supply
            True: that curtailment of request is shared among all demands proportional to it's demand.
            False: curtailment is divided equally among all demands despite their relative request rate
        outflows : list of Quantity rates
            The resulting deliveries from the source of each demand
        
        Methods
        -------
        
    """
    def __init__(self, supply, requests, proportional=True):
        """Initialize the amount and a list of requests with associated priorities for allocation"""
        self.supply = supply
        self._quantity_units = supply.units
        self._rate_units = requests[0].amount.units
        self.requests = requests
        self.proportional = proportional
        self.remainder = 0 * self._rate_units
        self.num_requests = len(requests)
        self.outflows = [0 * self._rate_units] * (self.num_requests + 1)
        self.remain_amount = self.supply
        self.allocated = [False] * self.num_requests
    
    def allocate(self):
        """Iterate over each demand and allocate supply."""
        # priorities = [self.requests[i].priority for i in range(len(self.requests))]
        # ord_priorities = priorities.copy()
        # ord_priorities.sort()
        ord_requests = sorted(self.requests, key=lambda x: x.priority)
        prior_match = [False] * self.num_requests
        count = range(self.num_requests)
        temp_demand = [0 * self._rate_units] * self.num_requests
        
        # Calculate the allocation quantities
        for request in ord_requests:
            current_priority = request.priority
            for i in count:
                prior_match[i] = not self.allocated[i] and current_priority == self.requests[i].priority
                temp_demand[i] = self.requests[i].amount if prior_match[i] else 0 * self._rate_units
            num_matches = sum(prior_match)
            # Only execute if there is a match
            if num_matches > 0:
                if num_matches == 1 or sum(temp_demand) * const.TS <= self.remain_amount:
                    # There is 1 priority match or amount is sufficient for requests with matching priority
                    dem_index_array = [1e10] * self.num_requests
                    for i in range(self.num_requests):
                        if not self.allocated[i] and current_priority == self.requests[i].priority:
                            dem_index_array[i] = i
                    dem_index = min(dem_index_array)
                    self.outflows[dem_index] = min(self.remain_amount / const.TS, self.requests[dem_index].amount)
                    self.remain_amount -= self.outflows[dem_index] * const.TS
                    self.allocated[dem_index] = True
                else:
                    # There are 2 or more priority matches and insufficient amount to meet requests
                    for i in range(self.num_requests):
                        if prior_match[i]:
                            self.outflows[i] = 0 * self._rate_units
                    if not self.proportional:
                        self.share_equal(prior_match, num_matches)
                    else: # Share proportional to demand
                        self.share_proportional(temp_demand, prior_match)
        self.outflows[self.num_requests] = self.remain_amount / const.TS
    
    def share_proportional(self, temp_demand, prior_match):
        for r in range(self.num_requests):
            fractional_demand = self.remain_amount / const.TS * temp_demand[r] / sum(temp_demand)
            if prior_match[r]:
                self.outflows[r] = fractional_demand
                self.allocated[r] = True
        self.remain_amount = 0 * self._quantity_units
    
    def share_equal(self, prior_match, num_matches):
        # share equally when the priorty is the same as others
        count = range(self.num_requests)
        fractional_demand = [0 * self._rate_units for i in count]
        
        # Iterate over remaining matches
        for match in range(num_matches):
            min_demand = min([self.requests[i].amount - fractional_demand[i] if prior_match[i] and not self.allocated[
                i] else 1e10 * self._rate_units for i in count])
            min_dem_id = min([i if prior_match[i] and not self.allocated[i] and self.requests[i].amount - fractional_demand[
                i] == min_demand else 1e10 for i in count])
            actual_demand = min(self.remain_amount / (num_matches * const.TS), min_demand)
            for d in count:
                if prior_match[d] and not self.allocated[d]:
                    fractional_demand[d] += actual_demand
                    if d == min_dem_id or actual_demand < min_demand:
                        self.allocated[d] = True
                        self.outflows[d] = fractional_demand[d]
            self.remain_amount -= num_matches * actual_demand * const.TS
            num_matches -= 1
