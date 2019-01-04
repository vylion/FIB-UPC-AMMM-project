#!/usr/bin/env python3


import copy
import time


class Change(object):
    def __init__(self, service, newBus=None, newDriver=None):
        self.service = service
        self.newBus = newBus
        self.newDriver = newDriver


class LocalSearch(object):
    def __init__(self, config):
        self.enabled = config.localSearch
        self.nhStrategy = config.neighborhoodStrategy
        self.policy = config.policy

        self.elapsedTime = 0
        self.iterations = 0

    def createNeighborSolution(self, solution, changes=[]):
        # unassign the tasks specified in changes
        # and reassign them to the new CPUs

        newSolution = copy.deepcopy(solution)
        feasible = True

        for change in changes:
            s, nb, nd = (change.service,
                         change.newBus, change.newDriver)
            solution.unassign(s)
            feasible = solution.assign(nb, nd, s)
            if not feasible:
                return None

        return newSolution

    def getSortedAssignmentsByCost(self, solution):
        buses = solution.buses
        drivers = solution.drivers
        services = solution.services

        assignments = []

        for sid, service in services.items():
            if not service.assigned:
                continue
            bus = buses[service.bus]
            driver = drivers[service.driver]

            assignment = (service, bus, driver,
                          service.getCost(buses, drivers))
            assignments.append(assignment)

        if self.policy == "BestImprovement":
            return assignments

        assignments.sort(key=lambda assignment: assignment[-1], reverse=True)
        return assignments

    def exploreNeighborhood(self, solution):
        bestNeighbor = solution
        bestCost = solution.updateCost()
        changes = []

        if self.nhStrategy == "Reassignment":
            assignments = self.getSortedAssignmentsByCost(solution)

            for assignment in assignments:
                service, oldBus, oldDriver, _ = assignment

                for bid, newBus in solution.buses.items():
                    for did, newDriver in solution.buses.items():
                        changes.append(Change(service,
                                              newBus, newDriver))

                        neighbor = self.createNeighborSolution(solution,
                                                               changes)
                        if neighbor is not None:
                            cost = neighbor.updateCost()
                            if cost < bestCost:
                                if self.policy == "FirstImprovement":
                                    return neighbor
                                bestNeighbor = neighbor
                                bestCost = cost

        elif self.nhStrategy == "Exchange":
            assignments = self.getSortedAssignmentsByCost(solution)

            for i in range(len(assignments)):
                for j in range(len(assignments)-1, -1, -1):
                    if i >= j:
                        continue
                    s1, b1, d1, _ = assignments[i]
                    s2, b2, d2, _ = assignments[j]

                    changes.append(Change(s2, b1, d1))
                    changes.append(Change(s1, b2, d2))

                    neighbor = self.createNeighborSolution(solution, changes)
                    if neighbor is not None:
                        cost = neighbor.updateCost()
                        if cost < bestCost:
                            if self.policy == "FirstImprovement":
                                return neighbor
                            else:
                                bestNeighbor = neighbor
                                bestCost = cost

        return bestNeighbor

    def run(self, solution):
        if not self.enabled:
            return solution

        if not solution.isFeasible():
            return solution

        bestSolution = solution
        bestCost = solution.updateCost()

        iterations = 0
        keepIterating = True

        startEvalTime = time.time()

        while keepIterating:
            keepIterating = False
            iterations += 1
            neighbor = self.exploreNeighborhood(bestSolution)
            cost = neighbor.updateCost()
            if cost < bestCost:
                bestSolution = neighbor
                bestCost = cost
                keepIterating = True

        self.iterations += iterations
        self.elapsedTime += time.time() - startEvalTime

        return bestSolution

    def printPerformance(self):
        if not self.enabled:
            return

        avg_evalTimePerIteration = 0.0
        if(self.iterations != 0):
            avg_evalTimePerIteration = (1000.0 * self.elapsedTime / float(self.iterations))

        print('')
        print('Local Search Performance:')
        print('  Num. Iterations Eval.', self.iterations)
        print('  Total Eval. Time     ', self.elapsedTime, 's')
        print('  Avg. Time / Iteration', avg_evalTimePerIteration, 'ms')
