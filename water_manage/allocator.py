from inputs.constants import U, TS


class Allocator:
    """The Allocator is used to allocate multiple demands of a finite and limited source amount.
    
        Attributes
        ----------
        supply : Quantity
            The supply that is being allocated
        requests : list of Quantity rates
            Individual requests being made on the source
        priorities : list of int
            Priority of each of the demands where lower values indicates higher priority
        proportional : bool
            Flag for proportional curtailment if sum demands > supply
            True: that curtailment of request is shared among all demands proportional to it's demand.
            False: curtailment is divided equally among all demands despite their relative request rate
        outflows : list of Quantity rates
            The resulting deliveries from the source of each demand
        
        Methods
        -------
        
    """
    def __init__(self, supply, requests, priorities, proportional=True):
        """Initialize the amount and a list of requests with associated priorities for allocation"""
        self.supply = supply
        self._quantity_units = supply.units
        self._rate_units = requests.units
        self.requests = requests
        self.priorities = priorities
        self.proportional = proportional
        self.remainder = 0 * self._rate_units
        self.num_requests = len(requests)
        self.outflows = [0 * self._rate_units] * (self.num_requests + 1)
        self.remain_amount = self.supply
        self.allocated = [False] * self.num_requests
    
    def allocate(self):
        """Iterate over each demand and allocate supply."""
        ord_priorities = self.priorities.copy()
        ord_priorities.sort()
        prior_match = [False] * self.num_requests
        count = range(self.num_requests)
        temp_demand = [0 * self._rate_units] * self.num_requests
        
        # Calculate the allocation quantities
        for prior in range(len(self.priorities)):
            current_priority = ord_priorities[prior]
            for i in count:
                prior_match[i] = not self.allocated[i] and current_priority == self.priorities[i]
                temp_demand[i] = self.requests[i] if prior_match[i] else 0 * self._rate_units
            num_matches = sum(prior_match)
            # Only execute if there is a match
            if num_matches > 0:
                if num_matches == 1 or sum(temp_demand) * TS <= self.remain_amount:
                    # There is 1 priority match or amount is sufficient for requests with matching priority
                    dem_index = min([i if not self.allocated[i] and current_priority == self.priorities[i] else 1e10 for i in count])
                    self.outflows[dem_index] = min(self.remain_amount / TS, self.requests[dem_index])
                    self.remain_amount -= self.outflows[dem_index] * TS
                    self.allocated[dem_index] = True
                else:
                    # There are 2 or more priority matches and insufficient amount to meet requests
                    frac_demand = [0 * self._rate_units for i in count]
                    self.outflows = [self.outflows[i] if i == self.num_requests else 0 * self._rate_units if prior_match[i] else self.outflows[i] for i in range(len(self.outflows))]
                    if not self.proportional:
                        self.share_equal(prior_match, num_matches)
                    else: # Share proportional to demand
                        self.share_proportional(temp_demand, prior_match)
        self.outflows[self.num_requests] = self.remain_amount / TS
    
    def share_proportional(self, temp_demand, prior_match):
        for r in range(self.num_requests):
            frac_demand = self.remain_amount / TS * temp_demand[r] / sum(temp_demand)
            if prior_match[r]:
                self.outflows[r] = frac_demand
                self.allocated[r] = True
        self.remain_amount = 0 * self._quantity_units
    
    def share_equal(self, prior_match, num_matches):
        # share equally when the priorty is the same as others
        count = range(self.num_requests)
        frac_demand = [0 * self._rate_units for i in count]
        
        # Iterate over remaining matches
        for match in range(num_matches):
            min_demand = min([self.requests[i] - frac_demand[i] if prior_match[i] and not self.allocated[
                i] else 1e10 * self._rate_units for i in count])
            min_dem_id = min([i if prior_match[i] and not self.allocated[i] and self.requests[i] - frac_demand[
                i] == min_demand else 1e10 for i in count])
            actual_demand = min(self.remain_amount / (num_matches * TS), min_demand)
            for d in count:
                if prior_match[d] and not self.allocated[d]:
                    frac_demand[d] += actual_demand
                    if d == min_dem_id or actual_demand < min_demand:
                        self.allocated[d] = True
                        self.outflows[d] = frac_demand[d]
            self.remain_amount -= num_matches * actual_demand * TS
            num_matches -= 1
