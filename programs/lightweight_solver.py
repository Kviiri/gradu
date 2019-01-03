#a lightweight LCL problem synther. Works for binary problems only.
#usage: python lightweight_solver.py problemlist graphdef

from pycosat import solve
from sys import argv
from ast import literal_eval
from collections import defaultdict
from problemgen import int_to_problem

with open(argv[1]) as f:
    problemset = map(lambda x: int(x), f.readlines())

with open(argv[2]) as f:
    graphdef = defaultdict(list)
    for node in map(lambda x: literal_eval(x), f.readlines()):
        graphdef[node[0]].append(node[1])
i = 1
node_id = {}
for key in graphdef:
    node_id[key] = i
    i += 1

for problemint in problemset:
    clauselist = []
    #construct set of ineligible candidates
    ineligible = [x for x in int_to_problem(0xFFFFFFFF)
            if x not in int_to_problem(problemint)]
    for node in graphdef:
        for candidate in ineligible:
            newclause = []
            if candidate[0] == '0':
                newclause.append(node_id[node])
            else:
                newclause.append(-node_id[node])

            neighbor_contingencies = {'S': [], 'W': [], 'N': [], 'E': []}
            for neighbor in graphdef[node]:
                #print str(neighbor)
                neighbor_id = node_id[neighbor[1]]
                newclause.append(neighbor_id * 
                        (1 if candidate[1][neighbor[0]] == '0' else -1))
                neighbor_contingencies[neighbor[0]].append(neighbor_id)
            for direction in neighbor_contingencies:
                nodelist = neighbor_contingencies[direction]
                for first, second in zip(nodelist, nodelist[1:]):
                    clauselist.append([first, -second])
                    clauselist.append([-first, second])
            clauselist.append(newclause)
    if solve(clauselist) != u'UNSAT':
       print problemint 
