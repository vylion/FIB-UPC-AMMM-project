#!/usr/bin/env python3


# Validate instance attributes read from a DAT file.
# It validates the structure of the parameters read from the DAT file.
# It does not validate that the instance is feasible or not.
# Use Problem.checkInstance() function to validate the feasibility of the
# instance.
class ValidateInputData(object):
    @staticmethod
    def validate(data):
        # Validate that all input parameters were found
        for paramName in ['numServices', 'numDrivers', 'numBuses', 'maxBuses',
                          'services', 'drivers', 'buses']:
            if paramName not in data.__dict__:
                raise Exception('Parameter/Set({}) not contained in Input Data'
                                .format(str(paramName)))

        # Validate numServices
        numServices = data.numServices
        if not isinstance(numServices, int) or (numServices <= 0):
            raise Exception(('numServices{}) has to be a positive integer '
                             + 'value.').format(str(numServices)))

        # Validate numDrivers
        numDrivers = data.numDrivers
        if not isinstance(numDrivers, int) or (numDrivers <= 0):
            raise Exception(('numDrivers({}) has to be a positive integer '
                             + 'value.').format(str(numDrivers)))

        # Validate numBuses
        numBuses = data.numBuses
        if not isinstance(numBuses, int) or (numBuses <= 0):
            raise Exception(('numBuses({}) has to be a positive integer '
                             + 'value.').format(str(numBuses)))

        # Validate maxBuses
        maxBuses = data.maxBuses
        if not isinstance(maxBuses, int) or (maxBuses <= 0):
            raise Exception(('maxBuses({}) has to be a positive integer '
                             + 'value.').format(str(maxBuses)))

        # Validate services
        services = data.services
        if(len(services) != numServices):
            raise Exception(('Size of services({}) does not match with value '
                             + 'of numServices({}).')
                            .format(len(services), numServices))

        for value in services:
            if(not isinstance(value, str) or (len(value) <= 0)):
                raise Exception(('Invalid parameter value("{}") in services. '
                                 + 'Should be a string representing an '
                                 + 'OPL tuple.').format(value))

        # Validate drivers
        drivers = data.drivers
        if(len(drivers) != numDrivers):
            raise Exception(('Size of drivers({}) does not match with value '
                             + 'of numDrivers({}).')
                            .format(len(drivers), numDrivers))

        for value in drivers:
            if(not isinstance(value, str) or (len(value) <= 0)):
                raise Exception(('Invalid parameter value("{}") in drivers. '
                                 + 'Should be a string representing an '
                                 + 'OPL tuple.').format(value))

        # Validate buses
        buses = data.buses
        if(len(buses) != numBuses):
            raise Exception(('Size of buses({}) does not match with value '
                             + 'of numBuses({}).')
                            .format(len(buses), numBuses))

        for value in buses:
            if(not isinstance(value, str) or (len(value) <= 0)):
                raise Exception(('Invalid parameter value("{}") in buses. '
                                 + 'Should be a string representing an '
                                 + 'OPL tuple.').format(value))
