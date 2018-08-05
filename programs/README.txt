This is a little set of tools for creating, solving and synthetizing LCL problems (the latter for torodic grids only!)

To use these tools, you need:
 1) Python  (tested to work with 2.7.12)
 2) scipy to match (for problemgen only)
 3) bc2cnf (from https://users.ics.aalto.fi/tjunttil/circuits/)
 4) a SAT solver (tested to work with Minisat)


---

LCL definitions are files in the following form: the FIRST line is a comma-separated list of acceptable output labels. The following lines are in the form:
('r', {'N': 'g', 'E': 'g', 'S': 'g', 'W': 'g'})

where 'r' is the "center" label and the dict following it defines acceptable outputs for this particular tile.

---

Graph definitions are files where each line defines an edge in the following form:
('foo', ('N', 'bar'))

where 'foo' is the name of the origin node, 'N' is the "orientation" label of the edge and 'bar' is the name of the target node. Nodes do not have to be declared separately.

---

SYNTHESIS PROCESS

First, you need tiles of a large enough dimension for the algorithm to work. To output tiles of dimensions x times y for some k, do the following:

python newtilegen.py x y k

This outputs tiles as Python lists of tuples, one tile per line eg.
[(0,1)]
[(2,0)]
[(2, 0),(0, 0),(1, 1)]
etc...

Direct the output to a file.

Next, you need to turn the tiles into an adjacency graph:

python tile2graph.py tilefile x y

Where tilefile is the file containing the tiles, and x and y are the tiles' width and height. tile2graph.py outputs a graphdef representing the tile adjacency graph.

To get a circuit (cqt) representation of the problem, use lcl2circuit.py:

python lcl2circuit.py graphdef lcldef varmap

Where graphdef is the graph you want to solve the lcl for, lcldef is the problem you want to solve/synthetize for and varmap is a file in which you want to store the mapping between the tentatively human-readable LCL tile assignments and the (likely thousands) of cqt variables. It's useful for deciphering the solution later on. Again, directing the output to somewhere is highly recommended.

The cqt can then be converted into CNFSAT using bc2cnf, and then solved using a CNFSAT solver, eg. Minisat. If the SAT solver manages to solve the LCL for the given graph, you can decipher the ultimate solution (and, in case of synthesis, the algorithm) using decoder.py:

python decoder.py varmap cnf ass

Where varmap is the one output by lcl2circuit.py, cnf is the conjunctive normal form file constructed by bc2cnf and ass is the assignments produced by a SAT solver when it finds a solution. The output of decoder.py is lines in the form
('foo', 'bar')

Where 'foo' is the name of the node (as given in the graphdef) and 'bar' is the output label it receives in the solution found by the SAT solver.

