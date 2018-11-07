#produces a biased solution to an LCL problem according to one_prob

import pycosat
from sys import argv
from problemgen import int_to_problem
from random import shuffle, random

grid_side = int(argv[1]) 
grid_size = grid_side ** 2
lclint = int(argv[2])
one_prob = float(argv[3])

ineligible = [x for x in int_to_problem(0xFFFFFFFF)
        if x not in int_to_problem(lclint)]

fixed = [0] * (grid_size)

done_assignments = 0
nodeorder = range(1, grid_size + 1)
shuffle(nodeorder)

while done_assignments < grid_size:
    clauselist = []
    for i in range(1, grid_size + 1):
        if fixed[i-1] != 0:
            clauselist.append([i * fixed[i-1]])
        for tile in ineligible:
            newclause = []
            if tile[0] == '0':
                newclause.append(i)
            else:
                newclause.append(-i)
            
            evar = (i-1) / grid_side * grid_side + i % grid_side + 1
            wvar = (i-1) / grid_side * grid_side + (i - 2) % grid_side + 1
            svar = (i + grid_side - 1) % grid_size + 1
            nvar = (i - grid_side - 1) % grid_size + 1

            newclause.append(evar * (1 if tile[1]['E'] == '0' else -1))
            newclause.append(svar * (1 if tile[1]['S'] == '0' else -1))
            newclause.append(wvar * (1 if tile[1]['W'] == '0' else -1))
            newclause.append(nvar * (1 if tile[1]['N'] == '0' else -1))
            clauselist.append(newclause)
    #now we attempt to fix one variable and SAT it
    value_to_fix = 1 if random() < one_prob else -1
    var_to_fix = nodeorder[done_assignments]
    if pycosat.solve(clauselist + [[var_to_fix * value_to_fix]]) != u'UNSAT':
        fixed[var_to_fix-1] = value_to_fix
    elif pycosat.solve(clauselist + [[var_to_fix * value_to_fix * -1]]) == u'UNSAT':
        raise Exception("Grid deemed not satisfiable")
    else:
        fixed[var_to_fix-1] = value_to_fix * -1
    done_assignments += 1
    print "Assignments done: %s out of %s" % (done_assignments, grid_size)

for i in range(0, grid_side):
    line = []
    for j in range(0, grid_side):
        line.append(str(1 if fixed[i*grid_side + j] == 1 else 0))
    print "".join(line)
