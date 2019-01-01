
class Bus(object):
    def __init__(self, busId, capacity, priceMinute, priceKm):
        self.id = busId
        self.capacity = capacity
        self.priceMin = priceMinute
        self.priceKm = priceKm
        self.serving = {}
        self.cost = 0

    def add(self, service):
        # Check if new service overlaps with a different served route
        for sid, s in self.serving.items():
            if service.id in s.overlaps:
                # Found overlap. Service is not added
                return False
        # Check if bus can fit passengers
        if service.numPassengers > self.capacity:
            return False
        # No constraint violations found
        self.serving[service.id] = service
        # Update cost
        self.cost += (self.priceKm * service.km
                      + self.priceMin * service.duration)
        # Service has been added
        return True

    def remove(self, service):
        # Remove service (if not found, Error is raised)
        del self.serving[service.id]
        # Update cost
        self.cost -= (self.priceKm * service.km
                      + self.priceMin * service.duration)
        # Service has been removed
        return True

    def cost(self):
        return self.cost
