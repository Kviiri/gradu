from sys import argv
from ast import literal_eval

tiles = set()
with open(argv[1]) as f:
    for line in f.readlines():
        tiles.add(frozenset(one for one in literal_eval(line)))

tilewidth = int(argv[2])
tileheight = int(argv[3])
edges = []

for tile in tiles:
    top_tile = frozenset((x,y) for (x,y) in tile if y < tileheight-1)
    bot_tile = frozenset((x,y-1) for (x,y) in tile if y > 0)
    edges.append(str((str(top_tile), ('S', str(bot_tile)))))
    edges.append(str((str(bot_tile), ('N', str(top_tile)))))
    edges.append(str((str(frozenset((y, x) for (x,y) in top_tile)),
        ('E', str(frozenset((y,x) for (x,y) in bot_tile))))))
    edges.append(str((str(frozenset((y, x) for (x,y) in bot_tile)),
        ('W', str(frozenset((y,x) for (x,y) in top_tile))))))

for edge in edges:
    print edge
