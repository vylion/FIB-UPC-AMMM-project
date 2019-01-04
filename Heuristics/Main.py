#!/usr/bin/env python3


import argparse
import sys

from DATParser import DATParser
from ValidateInputData import ValidateInputData
from ValidateConfig import ValidateConfig
from Solver_Greedy import Solver_Greedy
# from Solver_GRASP import Solver_GRASP
from Problem import Problem
# from Solution import Solution


def run():
    try:
        argp = argparse.ArgumentParser(description='AMMM Final Project')
        argp.add_argument('configFile', help='configuration file path')
        args = argp.parse_args()

        print('AMMM Final Project')
        print('------------------')

        print('Reading Config file {}...'.format(args.configFile))
        config = DATParser.parse(args.configFile)
        ValidateConfig.validate(config)

        print('Reading Input Data file {}...'.format(config.inputDataFile))
        inputData = DATParser.parse(config.inputDataFile)
        print(repr(inputData.__dict__))
        inputData.buses = list(inputData.buses)
        inputData.drivers = list(inputData.drivers)
        inputData.services = list(inputData.services)
        ValidateInputData.validate(inputData)

        print('Creating Problem...')
        problem = Problem(inputData)

        # if(problem.checkInstance()):
        print('Solving Problem...')
        solver = None
        solution = None
        if(config.solver == 'Greedy'):
            solver = Solver_Greedy()
            solution = solver.solve(config, problem)
        elif(config.solver == 'GRASP'):
            pass
            # solver = Solver_GRASP()
            # solution = solver.solve(config, problem)

        solution.saveToFile(config.solutionFile)
        # else:
        #     print('Instance is infeasible.')
        #     solution = Solution.createEmptySolution(config, problem)
        #     solution.makeInfeasible()
        #     solution.saveToFile(config.solutionFile)

        return 0
    except Exception as e:
        print()
        print('Exception:', e)
        print()
        return 1


if __name__ == '__main__':
    sys.exit(run())
