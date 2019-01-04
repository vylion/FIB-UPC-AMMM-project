#!/usr/bin/env python3


class Driver(object):
    def __init__(self, driverId, maxTime, BM, CBM, CEM):
        self.id = driverId
        self.maxTime = maxTime
        self.workingHours = 0
        self.BM = BM
        self.CBM = CBM
        self.CEM = CEM
        self.serving = {}

    def add(self, service):
        # Check if new service overlaps with a different served route
        for sid, s in self.serving.items():
            if service.id in s.overlaps:
                # Found overlap. Service is not added
                return False
        # Check if new service is over the maximum working time
        if self.workingHours + service.duration > self.maxTime:
            return False
        # No constraint violations found
        self.serving[service.id] = service
        # Updating working time
        self.workingHours += service.duration
        # Service has been added
        return True

    def remove(self, service):
        # Remove service (if not found, Error is raised)
        del self.serving[service.id]
        # Updating working time
        self.workingHours -= service.duration
        # Service has been removed
        return True

    def getCost(self):
        cost = (min(self.workingHours, self.BM) * self.CBM
                + max(self.workingHours - self.BM, 0) * self.CEM)
        return cost

    def getBMHours(self):
        return min(self.workingHours, self.BM)

    def getOvertime(self):
        return max(0, self.workingHours - self.BM)
