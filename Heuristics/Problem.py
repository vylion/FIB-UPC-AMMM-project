from Bus import Bus
from Driver import Driver
from Service import Service


class Problem(object):
    def __init__(self, inputData):
        self.inputData = inputData

        nServices = inputData.numServices
        nBuses = inputData.numBuses
        nDrivers = inputData.numDrivers
        self.maxBuses = inputData.maxBuses

        self.buses = {}
        for busId in range(0, nBuses):
            # Assuming that each element of inputData.buses is a string,
            # remove initial and trailing "<...>", then split on ","
            busData = inputData.buses[busId].strip('<>').split(',')
            # Convert to numeral values
            for i in range(0, len(busData)):
                busData[i] = int(busData[i].strip())
            # Create element
            bus = Bus(busId, busData[0], busData[1], busData[2])
            self.buses[bus.id] = bus

        self.drivers = {}
        for driverId in range(0, nDrivers):
            # Assuming that each element of inputData.drivers is a string,
            # remove initial and trailing "<...>", then split on ","
            driverData = inputData.drivers[driverId].strip('<>').split(',')
            # Convert to numeral values
            for i in range(0, len(driverData)):
                try:
                    driverData[i] = int(driverData[i].strip())
                except ValueError:
                    driverData[i] = float(driverData[i].strip())
            # Create element
            driver = Driver(driverId, driverData[0], driverData[1],
                            driverData[2], driverData[3])
            self.drivers[driver.id] = driver

        self.services = {}
        for serviceId in range(0, nServices):
            # Assuming that each element of inputData.services is a string,
            # remove initial and trailing "<...>", then split on ","
            serviceData = inputData.services[serviceId].strip('<>').split(',')
            # Convert to numeral values
            for i in range(0, len(serviceData)):
                serviceData[i] = int(serviceData[i].strip())
            service = Service(serviceId, serviceData[0], serviceData[1],
                              serviceData[2], serviceData[3], self.services)
            self.services[service.id] = service

    # This method counts the number of serving buses
    def countBuses(self):
        count = 0
        for bid, bus in self.buses.items():
            count += 1 if len(bus.serving) > 0 else 0
        return count

    def getBuses(self):
        return list(self.buses.values())

    def getDrivers(self):
        return list(self.drivers.values())

    def getServices(self):
        return list(self.services.values())

    def checkInstance(self):
        # Number of serving buses should be less or equal than the maximum
        if self.countBuses() > self.maxBuses:
            return False
        # All services should be assigned to a bus and a driver
        for sid, service in self.services.items():
            if not service.assigned:
                return False
        # No bus should serve overlapping services
        # (Checked when assigning a bus to a service)
        # No bus should serve for more passengers than it can fit
        # (Checked when assigning a bus to a service)
        # No driver should serve overlapping services
        # (Checked when assigning a driver to a service)
        # No driver should work more than their maximum working time
        # (Checked when assigning a driver to a service)

        # No constraint violations found
        return True
