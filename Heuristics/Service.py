#!/usr/bin/env python3


class Service(object):
    def __init__(self, servId, start, duration, km, numPassengers, services):
        self.id = servId
        self.start = start
        self.duration = duration
        self.end = start + duration
        self.km = km
        self.numPassengers = numPassengers
        self.overlaps = set()
        # Check if new service overlaps with any existing ones
        for sid, service in services.items():
            if self.overlapping(service):
                service.overlaps.add(self.id)
                self.overlaps.add(sid)
        # Current assignment status
        self.assigned = False

    def overlapping(self, s2):
        one = s2.start >= self.start and s2.start < self.end
        two = self.start >= s2.start and self.start < s2.end
        return one or two

    def assign(self, bus, driver):
        # Check if service isn't already assigned
        if self.assigned:
            return False
        # Store assigned bus and driver ids
        self.bus = bus.id
        self.driver = driver.id
        # Assign this service to bus and driver
        success = bus.add(self)
        # Check if bus was assigned correctly
        if not success:
            return False
        success = driver.add(self)
        # Check if driver was assigned correctly
        if not success:
            bus.remove(self)
            return False
        # Current assignment status
        self.assigned = True
        return True

    def unassign(self, buses, drivers):
        # Check if service is already unasigned
        if not self.assigned:
            return False
        # Get assigned bus and driver ids
        bid = self.bus
        did = self.driver
        # Remove asigned ids
        self.bus = None
        self.driver = None
        # Remove service from bus and driver assignments
        buses[bid].remove(self)
        drivers[did].remove(self)
        # Current assignment status
        self.assigned = False
        return True

    def changeBus(self, bus, buses):
        # Check if service is already unasigned
        if not self.assigned:
            return False
        # Get assigned bus id
        bid = self.bus
        # Assign this service to the new bus
        success = bus.add(self)
        # Check if bus was assigned correctly
        if not success:
            return False
        # Remove assignment from old bus
        buses[bid].remove(self)
        return True

    def changeDriver(self, driver, drivers):
        # Check if service is already unasigned
        if not self.assigned:
            return False
        # Get assigned bus id
        did = self.bus
        # Assign this service to the new bus
        success = driver.add(self)
        # Check if bus was assigned correctly
        if not success:
            return False
        # Remove assignment from old bus
        drivers[did].remove(self)
        return True

    def getCost(self, buses, drivers):
        bus = buses[self.bus]
        driver = drivers[self.driver]
        return (bus.getCost() + driver.getCost())

    def resources(self):
        return self.duration * self.km * (self.numPassengers / 100)
