#!/usr/bin/env python3


import os


# Validate config attributes read from a DAT file.
class ValidateConfig(object):
    @staticmethod
    def validate(data):
        # Validate that mandatory input parameters were found
        for paramName in ['inputDataFile', 'solutionFile', 'solver']:
            if paramName not in data.__dict__:
                raise Exception(('Parameter/Set({}) not contained in '
                                 + 'Configuration').format(str(paramName)))

        # Validate input data file
        inputDataFile = data.inputDataFile
        if len(inputDataFile) == 0:
            raise Exception('Value for inputDataFile is empty')
        if not os.path.exists(inputDataFile):
            raise Exception('inputDataFile({}) does not exist'
                            .format(inputDataFile))

        # Validate solution file
        solutionFile = data.solutionFile
        if len(solutionFile) == 0:
            raise Exception('Value for solutionFile is empty')

        # Validate verbose
        verbose = False
        if 'verbose' not in data.__dict__:
            verbose = data.verbose
            if (not isinstance(verbose, (bool))
                    or (verbose not in [True, False])):
                raise Exception('verbose({}) has to be a boolean value.'
                                .format(str(verbose)))
        else:
            data.verbose = verbose

        # Validate solver and per-solver parameters
        solver = data.solver
        if solver == 'Greedy':
            # Validate that mandatory input parameters for Greedy solver
            # were found
            for paramName in ['localSearch']:
                if paramName not in data.__dict__:
                    raise Exception(('Parameter/Set({}) not contained in '
                                     + 'Configuration. Required by Greedy '
                                     + 'solver.').format(str(paramName)))

            # Validate localSearch
            localSearch = data.localSearch
            if (not isinstance(localSearch, (bool))
                    or (localSearch not in [True, False])):
                raise Exception('localSearch({}) has to be a boolean value.'
                                .format(str(localSearch)))

        elif solver == 'GRASP':
            # Validate that mandatory input parameters for GRASP solver
            # were found
            for paramName in ['maxExecTime', 'alpha', 'localSearch']:
                if paramName not in data.__dict__:
                    raise Exception('Parameter/Set({}) not contained in '
                                    + 'Configuration. Required by GRASP '
                                    + 'solver.'.format(str(paramName)))

            # Validate maxExecTime
            maxExecTime = data.maxExecTime
            if (not isinstance(maxExecTime, (int, float))
                    or (maxExecTime <= 0)):
                raise Exception('maxExecTime({}) has to be a positive float '
                                + 'value.'.format(str(maxExecTime)))

            # Validate alpha
            alpha = data.alpha
            if(not isinstance(alpha, (int, float))
                    or (alpha < 0) or (alpha > 1)):
                raise Exception('alpha({}) has to be a float value in range '
                                + '[0, 1].'.format(str(alpha)))

            # Validate localSearch
            localSearch = data.localSearch
            if(not isinstance(localSearch, (bool))
                    or (localSearch not in [True, False])):
                raise Exception('localSearch({}) has to be a boolean value.'
                                .format(str(localSearch)))

        else:
            raise Exception('Unsupported solver specified({}) in '
                            + 'Configuration. Supported solvers are: Greedy '
                            + 'and GRASP.'.format(str(solver)))

        if(data.localSearch):
            # Validate that mandatory input parameters for local search
            # were found
            for paramName in ['neighborhoodStrategy', 'policy']:
                if paramName not in data.__dict__:
                    raise Exception('Parameter/Set({}) not contained in '
                                    + 'Configuration. Required by '
                                    + 'Local Search.'.format(str(paramName)))

            # Validate neighborhoodStrategy
            neighborhoodStrategy = data.neighborhoodStrategy
            if neighborhoodStrategy not in ['Reassignment', 'Exchange']:
                raise Exception('neighborhoodStrategy({}) has to be one of '
                                + '[Reassignment, Exchange].'
                                .format(str(neighborhoodStrategy)))

            # Validate policy
            policy = data.policy
            if policy not in ['BestImprovement', 'FirstImprovement']:
                raise Exception('policy({}) has to be one of '
                                + '[BestImprovement, FirstImprovement].'
                                .format(str(policy)))
