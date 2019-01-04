#!/usr/bin/env python3


import random
import time
from Solver import Solver
from Solution import Solution
from LocalSearch import LocalSearch


# Inherits from a parent abstract solver.
class Solver_GRASP(Solver):
    def selectCandidate(self, alpha, candidateList):
        if len(candidateList) == 0:
            return None

        candidateList.sort(key=lambda candidate: candidate[-1], reverse=False)
        minCost = candidateList[0][-1]
        maxCost = candidateList[-1][-1]

        boundaryCost = minCost + (maxCost - minCost) * alpha
        maxIndex = 0
        for c in candidateList:
            if c[-1] > boundaryCost:
                break
            maxIndex += 1

        rcl = candidateList[0:maxIndex]
        if len(rcl) == 0:
            return None

        return random.choice(rcl)

    def greedyRandomizedConstruction(self, config, problem):
        solution = Solution.createEmptySolution(config, problem)
        services = solution.getServices()
        services.sort(key=lambda service: service.resources(), reverse=True)

        elapsedTime = 0
        evaluatedCandidates = 0

        for service in services:
            (candidateList,
             serviceElapsedTime,
             serviceNumCandidates) = solution.findFeasibleAssignments(service.id)

            elapsedTime += serviceElapsedTime
            evaluatedCandidates += serviceNumCandidates

            if len(candidateList) == 0:
                solution.makeInfeasible()
                break

            # Select an assignment
            candidate = self.selectCandidate(config.alpha, candidateList)
            if candidate is None:
                break

            solution.assign(candidate[1], candidate[2], candidate[0])

        return (solution, elapsedTime, evaluatedCandidates)

    def solve(self, config, problem):
        bestSolution = Solution.createEmptySolution(config, problem)
        bestSolution.makeInfeasible()
        bestCost = bestSolution.cost
        self.startTimeMeasure()
        self.writeLogLine(bestCost, 0)

        total_elapsedEvalTime = 0
        total_evaluatedCandidates = 0

        localSearch = LocalSearch(config)
        alpha = config.alpha

        iteration = 0
        while time.time() - self.startTime < config.maxExecTime:
            iteration += 1

            # force first iteration as a Greedy execution (alpha == 0)
            if iteration == 1:
                config.alpha = 0

            (solution,
             elapsedEvalTime,
             evaluatedCandidates) = self.greedyRandomizedConstruction(config,
                                                                      problem)

            total_elapsedEvalTime += elapsedEvalTime
            total_evaluatedCandidates += evaluatedCandidates

            # recover original alpha
            if iteration == 1:
                config.alpha = alpha

            if not solution.isFeasible():
                continue

            solution = localSearch.run(solution)

            solutionCost = solution.updateCost()
            if solutionCost < bestCost:
                bestSolution = solution
                bestCost = solutionCost
                self.writeLogLine(bestCost, iteration)

        self.writeLogLine(bestCost, iteration)
        avg_evalTimePerCandidate = 0.0
        if(total_evaluatedCandidates != 0):
            avg_evalTimePerCandidate = 1000.0 * total_elapsedEvalTime / float(total_evaluatedCandidates)

        print('')
        print('Greedy Candidate Evaluation Performance:')
        print('  Num. Candidates Eval.', total_evaluatedCandidates)
        print('  Total Eval. Time     ', total_elapsedEvalTime, 's')
        print('  Avg. Time / Candidate', avg_evalTimePerCandidate, 'ms')

        localSearch.printPerformance()

        return solution
