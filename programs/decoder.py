from sys import argv
from ast import literal_eval

with open(argv[1]) as f:
    vartolabel = { v: k for k, v in literal_eval(f.readline()).iteritems()}

with open(argv[2]) as f:
    predtovar = {}
    for line in f.readlines():
        if line.startswith("c"):
            if "<->" not in line:
                continue
            splitline = line.split()
            if splitline[1].startswith("x"):
                predtovar[splitline[3]] = splitline[1]
        else:
            break

with open(argv[3]) as f:
    f.readline()
    cnfvars = filter(lambda x: not x.startswith("-"), f.readline().split())

for var in cnfvars:
    if var in predtovar:
        print vartolabel[predtovar[var]]
