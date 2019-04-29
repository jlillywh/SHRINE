from inputs.constants import U, TS


class Allocator:
    """The Allocator is used to allocate multiple demands of a finite and limited source amount.
    
        Attributes
        ----------
        supply : Quantity
            The supply that is being allocated
        demands : list of Quantity rates
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
    def __init__(self, supply, demands, priorities, proportional=True):
        """Initialize the amount and a list of demands with associated priorities for allocation"""
        self.supply = supply
        self._quantity_units = supply.units
        self._rate_units = demands.units
        self.demands = demands
        self.priorities = priorities
        self.proportional = proportional
        self.remainder = 0 * self._rate_units
        self.num_requests = len(demands)
        self.outflows = [0 * self._rate_units] * self.num_requests
        
    def allocate(self):
        """Iterate over each demand and allocate supply."""
        remain_amount = self.supply
        ord_priorities = self.priorities.sort()
        allocated = [False] * self.num_requests
        prior_match = [False] * self.num_requests
        num_allocations = 0
        num_demands = 0
        num_matches = 0
        temp_demand = [0 * self._rate_units] * self.num_requests
        current_priority = 0
        dem_index = 0
        # Calculate the allocation quantities
        for prior in self.priorities:
            current_priority = ord_priorities[prior]
            prior_match = [not allocated[i] and current_priority == self.priorities[i] for i in allocated]
            num_matches = sum([1 if prior_match[i] else 0 for i in prior_match])
            temp_demand = [self.demands[i] if prior_match[i] else 0 * self._rate_units for i in prior_match]
            # Only execute if there is a match
            if num_matches > 0:
                if num_matches == 1 or sum(temp_demand) * TS <= remain_amount:
                    # There is 1 priority match or amount is sufficient for demands with matching priority
                    dem_index = min([i if not allocated[i] and current_priority == self.priorities[i] else 1e10 for i in allocated])
                    self.outflows = [min(remain_amount / TS, self.demands[dem_index]) for i in self.demands]
                    remain_amount -= self.outflows[dem_index] * TS
                    allocated[dem_index] = True
                else:
                    # There are 2 or more priority matches and insufficient amount to meet demands
                    frac_demand = [0 * self._rate_units for i in self.demans]
                    self.outflows = [self.outflows[i] if i == self.num_requests else 0 if prior_match[i] else self.outflow[i] for i in prior_match]
                    if not self.proportional:
                        # share equally when the priorty is the same as others
                        min_demand = 0 * self._rate_units
                        min_dem_id = 0
                        actual_demand = 0 * self._rate_units
                        iterate = num_matches
                        
                        # Iterate over remaining matches
                        for match in self.demands:
                            min_demand = min([self.demands[i] - frac_demand[i] if prior_match[i] and not allocated[i] else 1e10 for i in frac_demand])
                            min_dem_id = min([i if prior_match[i] and not allocated[i] and self.demands[i] - frac_demand[i] == min_demand else 1e10 for i in self.demands])
                            actual_demand = min(remain_amount / (num_matches * TS), min_demand)
                            for d in frac_demand:
                                if prior_match[d] and not allocated[d]:
                                    frac_demand[d] += actual_demand
                                    if d == min_dem_id or actual_demand < min_demand:
                                        allocated[d] = True
                                        self.outflows[d] = frac_demand[d]
                            remain_amount -= num_matches * actual_demand
                            num_matches -= 1
                        else: # Share proportional to demand
                            frac_demand = [remain_amount / TS * temp_demand[i] / sum(temp_demand) for i in frac_demand]
                            for dem in frac_demand:
                                if prior_match[dem]:
                                    self.outflows[dem] = frac_demand[dem]
                                    allocated[dem] = True
                            remain_amount = 0 * self._quantity_units
        self.outflows[len(self.demands) + 1] = remain_amount / TS
                    
                    
                    
                    
            
            