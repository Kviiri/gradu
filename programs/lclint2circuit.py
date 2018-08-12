#!/usr/bin/python

#modified version of lcl2circuit.py
#produces lcldef for binary lcl itself, using an integer input (lclint)
#assumes symbols to be "0" and "1"

#usage: python lcl2circuit.py graphdef lclint variablemap > output

from sys import argv
from ast import literal_eval
from itertools import combinations
from collections import defaultdict
from problemgen import int_to_problem

with open(argv[1]) as f:
    graphdef = defaultdict(list)
    for node in map(lambda x: literal_eval(x), f.readlines()):
        graphdef[node[0]].append(node[1])

outputlabels = ['0', '1']
lcldef = int_to_problem(int(argv[2]))


i = 1
varmap = {}
exclusivityclauses = []
for node in graphdef:
    singlelabelclause = []
    for label in outputlabels:
        varmap[(node, label)] = "x%d" % i
        singlelabelclause.append("x%d" % i)
        i = i + 1
    exclusivityclauses.append("[1,1](" + ",".join(singlelabelclause) + ")")

clauselist = []
candidatemap = {}
i = 1
j = 1

#x%d == node has particular label
#t%d == node matches an entire LCL tile
#n%d == node is correct (matches any LCL tile)

rootclause = []
rootclause.append("AND(%s)" % ",".join(exclusivityclauses))
for node in graphdef:
    orclause = []
    for lcltile in lcldef:
        andclause=[]
        #candidatemap a numeric key for node n being centered by lcltile l
        #it's used to create working circuit clauses for exactly one tile matching
        andclause.append("t%d := AND(%s" % (i, varmap[(node, lcltile[0])]))
        orclause.append("t%d" % i)
        i = i + 1
        for edge in graphdef[node]:
            andclause.append(str(varmap[edge[1], lcltile[1][edge[0]]]))
        clauselist.append(",".join(andclause) + ")")
    clauselist.append("n%d := OR(" % j + ",".join(orclause) + ")")
    rootclause.append("n%d" % j)
    j = j + 1
clauselist.append("a := AND(" + ",".join(rootclause) + ")")
clauselist.append("ASSIGN a;")
print("BC1.1")
print(";\n".join(clauselist))

if len(argv) > 3:
    with open(argv[3], "w") as f:
        f.write(str(varmap))
