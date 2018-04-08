from sys import argv
from ast import literal_eval

#a helper tool for printing 2d arrays as grids
#expecting input in form of tuples ('(x,y)', 'l') where x, y are coordinates (starting from 0)
#  and l is label

x = int(argv[1])
y = int(argv[2])

grid =[['?' for i in range(x)] for j in range(y)]

with open(argv[3]) as f:
    for line in f.readlines():
        tup = literal_eval(line)
        grid[literal_eval(tup[0])[0]][literal_eval(tup[0])[1]] = tup[1]

print "\n".join(" ".join(row) for row in grid)
