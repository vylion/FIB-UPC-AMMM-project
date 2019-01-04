#!/usr/bin/env python3


from Solver import Solver
from Solution import Solution
from LocalSearch import LocalSearch


# Inherits from a parent abstract solver.
class Solver_Greedy(Solver):
    def greedyConstruction(self, config, problem):
        solution = Solution.createEmptySolution(config, problem)

        services = solution.getServices()
        services.sort(key=lambda service: service.resources(), reverse=True)

        elapsedTime = 0
        evaluatedCandidates = 0

        for service in services:
            (feasibleAssignments,
             serviceElapsedTime,
             serviceNumCandidates) = solution.findFeasibleAssignments(service)

            elapsedTime += serviceElapsedTime
            evaluatedCandidates += serviceNumCandidates

            # Choose assignment with minimum cost
            minCost = float('infinity')
            chosen = None
            for assignment in feasibleAssignments:
                if assignment[-1] < minCost:
                    minCost = assignment[-1]
                    chosen = assignment

            if chosen is None:
                solution.makeInfeasible()

            solution.assign(chosen[1], chosen[2], chosen[0])

        return (solution, elapsedTime, evaluatedCandidates)

    def solve(self, config, problem):
        self.startTimeMeasure()
        self.writeLogLine(float('infinity'), 0)

        (solution,
         elapsedEvalTime,
         evaluatedCandidates) = self.greedyConstruction(config, problem)
        self.writeLogLine(solution.updateCost(), 1)

        localSearch = LocalSearch(config)
        solution = localSearch.run(solution)

        self.writeLogLine(solution.updateCost(), 1)

        avg_evalTimePerCandidate = 0.0
        if (evaluatedCandidates != 0):
            avg_evalTimePerCandidate = 1000.0 * elapsedEvalTime / float(evaluatedCandidates)

        print('')
        print('Greedy Candidate Evaluation Performance:')
        print('  Num. Candidates Eval.', evaluatedCandidates)
        print('  Total Eval. Time     ', elapsedEvalTime, 's')
        print('  Avg. Time / Candidate', avg_evalTimePerCandidate, 'ms')

        localSearch.printPerformance()

        return solution
