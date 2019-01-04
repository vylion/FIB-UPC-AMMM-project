#!/usr/bin/env python3


import time
from Problem import Problem


class Solution(Problem):
    @staticmethod
    def createEmptySolution(config, problem):
        solution = Solution(problem.inputData)
        solution.setVerbose(config.verbose)
        return(solution)

    def __init__(self, inputData):
        super(Solution, self).__init__(inputData)

        self.feasible = True
        self.cost = 0

    def setVerbose(self, verbose):
        self.verbose = verbose

    def isFeasible(self):
        self.checkInstance()
        if not self.feasible:
            self.cost = float('infinity')
        return self.feasible

    def makeInfeasible(self):
        self.feasible = False
        self.cost = float('infinity')

    # This method both checks feasability and assigns if feasible
    def assign(self, bus, driver, service):
        # Do not attempt if we know this solution is already feasible
        if not self.feasible:
            self.log("Unable to do assignment. "
                     + "Solution is already unfeasible.")
            return False
        # Check assignment feasability
        feasible = service.assign(bus, driver)
        if not feasible:
            self.log("Unable to assign bus {} and driver {} to service {}."
                     .format(bus.id, driver.id, service.id))
            return False
        return True

    def unassign(self, service):
        feasible = service.unassign(self.buses, self.drivers)
        if not feasible:
            self.log("Service is already unassigned.")
            return False
        return True

    def changeBus(self, service, bus):
        success = service.changeBus(bus, self.buses)
        if not success:
            self.log("Unable to change bus {} to bus {} in service {}."
                     .format(service.bus, bus.id))
            return False
        return True

    def changeDriver(self, service, driver):
        success = service.changeDriver(driver, self.drivers)
        if not success:
            self.log("Unable to change driver {} to driver {} in service {}."
                     .format(service.driver, driver.id))
            return False
        return True

    def updateCost(self):
        cost = 0
        for _, bus in self.buses.items():
            cost += bus.getCost()
        for _, driver in self.drivers.items():
            cost += driver.getCost()
        self.cost = cost
        return cost

    def findFeasibleAssignments(self, service):
        startEvalTime = time.time()
        evaluatedCandidates = 0

        feasibleAssignments = []
        for bid, bus in self.buses.items():
            for did, driver in self.drivers.items():
                feasible = self.assign(bus, driver, service)

                evaluatedCandidates += 1
                if not feasible:
                    continue

                assignment = (service, bus, driver, self.updateCost())
                feasibleAssignments.append(assignment)

                self.unassign(service)
        elapsedTime = time.time() - startEvalTime
        return (feasibleAssignments, elapsedTime, evaluatedCandidates)

    def findBestFeasibleAssignment(self, service):
        best = (service, None, None, float('infinity'))

        for bid, bus in self.buses.items():
            for did, driver in self.drivers.items():
                feasible = self.assign(bus, driver, service)
                if not feasible:
                    continue
                cost = self.updateCost()
                if cost < best[-1]:
                    best = (service, bus, driver, cost)
                self.unassign(service)
        return best

    def log(self, s):
        if self.verbose:
            print(s)

    def __str__(self):
        s = "z = {};\n\n".format(self.updateCost())

        nBuses = self.inputData.numBuses
        nServices = self.inputData.numServices
        nDrivers = self.inputData.numDrivers

        # busServesService

        busServesService = []
        for b in range(0, nBuses):
            bs = [0] * nServices
            busServesService.append(bs)

        for bid, bus in self.buses.items():
            for sid, service in bus.serving.items():
                busServesService[bid][sid] = 1

        s += "busServesService = [\n"
        for b in busServesService:
            s += "\t[ "
            for bs in b:
                s += str(bs) + " "
            s += "]\n\n"

        # DriverServesService

        driverServesService = []
        for d in range(0, nDrivers):
            ds = [0] * nServices
            driverServesService.append(ds)

        for did, driver in self.buses.items():
            for sid, service in driver.serving.items():
                driverServesService[did][sid] = 1

        s += "driverServesService = [\n"
        for d in driverServesService:
            s += "\t[ "
            for ds in d:
                s += str(ds) + " "
            s += "]\n\n"

        # DriverHours (non-overtime hours)

        driverHours = [0] * nDrivers
        for did, driver in self.drivers.items():
            driverHours[did] = driver.getBMHours()

        s += "driverHours [ "
        for d in driverHours:
            s += str(d) + " "
        s += "]\n\n"

        # driverOvertime (overtime hours)

        driverOvertime = [0] * nDrivers
        for did, driver in self.drivers.items():
            driverOvertime[did] = driver.getOvertime()

        s += "driverOvertime [ "
        for d in driverOvertime:
            s += str(d) + " "
        s += "]\n\n"

        return s

    def saveToFile(self, filePath):
        f = open(filePath, 'w')
        f.write(self.__str__())
        f.close()
