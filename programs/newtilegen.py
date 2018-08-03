from sys import argv
from itertools import product

def create_columns(n, k):
    #valid: set of sets of tuples representing valid columns
    #empty column is always valid
    valid = {frozenset()}
    #we start with empty column as a possibility
    old = {frozenset()}
    for number_of_ones in range(1, -(-n//(k+1))+1):
        new = set()
        #try to expand each old tile
        for col in old:
            #in each possible i
            accepted_post = set() 
            accepted_pre = set()
            l = 0
            for i in range(0, n):
                if i not in col and l == 0:
                    accepted_post.update(col, {i})
                elif i in col:
                    l = k
                else:
                    l = l - 1
            l = 0
            for i in reversed(range(0, n)):
                if i not in col and l == 0:
                    accepted_pre.update(col, {i})
                elif i in col == 1:
                    l = k
                else:
                    l = l - 1
            #add successful lines to new if they're not there yet
            new.update(map(lambda x: frozenset(col.union({x})), accepted_pre.intersection(accepted_post)))
        valid.update(new)
        old = new
    return valid

def extend_valid(oneSet, candidate_columns, tilewidth, tileheight, max_width, k):
    candidate_columns = frozenset(frozenset((tilewidth-1, x) for x in y) for y in candidate_columns)
    valid_columns = set() 
    #0: can be 0 or 1
    #1: can only be 1
    #-1: can't be 1
    roweligibilities = [0]*tileheight
    #mark mandatory zeroes -1
    for one in oneSet:
        if one[0] >= tilewidth - 1 - k:
            i = 0
            bypassed = False
            while i < tileheight:
                #todo: optimize if needed
                if is_manhattan_close(one, (tilewidth-1, i), k):
                    bypassed = True
                    roweligibilities[i] = -1
                elif bypassed:
                    break
                i = i + 1
    if tilewidth-2*k > 0:
        #next we add the nondominated zeroes if the tile has any
        #contains (x, y) of all nondominated zeroes
        nondominated_candidates = set((tilewidth-1, y) for y in range(k, tileheight-k))
        #while instead of for, for juju optimizations
        for one in oneSet:
            delete_set = set()
            #only ones close enough to the edge to count
            if(one[0] >= tilewidth - k - 1):
                for nondom in nondominated_candidates:
                    if is_manhattan_close(nondom, one, k):
                        delete_set.add(nondom)
            nondominated_candidates -= delete_set
            if not nondominated_candidates:
                break
        for nondom in nondominated_candidates:
            roweligibilities[nondom[1]] = 1
    for column in candidate_columns:
        is_valid = True
        for row in range(0, tileheight):
            if roweligibilities[row] == -1 and (tilewidth-1, row) in column:
                is_valid = False
                break
            if roweligibilities[row] == 1 and (tilewidth-1, row) not in column:
                is_valid = False
                break
        if is_valid:
            valid_columns.add(column)
    valid_columns = filter(lambda column: backtrack_set_hitting(oneSet.union(column),
        get_nondominated_zeroes(oneSet.union(column), tilewidth, tileheight, max_width, k),
        tilewidth, tileheight, k), valid_columns)
    return map(lambda x: oneSet.union(x), valid_columns)

def get_nondominated_zeroes(tile, tilewidth, tileheight, max_width, k):
    #step 1: find non-dominated zeroes at most k away from the edge
    #we ignore the right edge until close to the final size
    nondominated_zeroes = {c for c in product(range(0, tilewidth), range(0, tileheight))}
    nondominated_zeroes = filter(lambda c: not inside_area(c, k, k, max_width-k, tileheight-k), nondominated_zeroes)
    for one in tile:
        nondominated_zeroes = filter(lambda nondom: not is_manhattan_close(nondom, one, k), nondominated_zeroes)
        if not nondominated_zeroes:
            break
    return nondominated_zeroes

def get_manhattan(point, k):
    return set(filter(lambda c: is_manhattan_close(c, point, k),
        product(range(point[0] - k, point[0] + k + 1), range(point[1] - k, point[1] + k + 1))))

def is_manhattan_close(point1, point2, k):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1]) <= k

def inside_area(point, x, y, width, height):
    return point[0] >= x and point[0] < width and point[1] >= y and point[1] < height

def nondominated_zero_neighborhoods(tilewidth, tileheight, nondominated_zeroes, k, exclusionset):
    ret = []
    for zero in nondominated_zeroes:
        ret.append(set(filter(lambda c: not inside_area(c, 0, 0, tilewidth, tileheight),
            get_manhattan(zero, k))))
    return ret

def get_exclusionset(ones, tilewidth, tileheight, k):
    exclusionset = set()
    for one in ones:
        exclusionset.update(filter(lambda c: not inside_area(one, 0, 0, tilewidth, tileheight),
            get_manhattan(one, k)))
    return exclusionset

def backtrack_set_hitting(ones, nondominated_zeroes, tilewidth, tileheight, k):
    if not nondominated_zeroes:
        #no nondominated zeroes, no problem!
        return True
    exclusionset = get_exclusionset(ones, tilewidth, tileheight, k)
    neighborhoods = nondominated_zero_neighborhoods(tilewidth, tileheight, nondominated_zeroes, k, exclusionset)
    for i in range(0, len(neighborhoods)):
        neighborhoods[i] = neighborhoods[i] - exclusionset
    #initialize stack with candidate "ones" from an arbitrary nondominated zero
    stack = [{coord} for coord in neighborhoods[0]]
    while stack:
        #state is a set of ones
        state = stack.pop()
        #we check which neighborhoods we have hit
        unhit_neighborhoods = [x for x in neighborhoods if all([y not in state for y in x])]
        if not unhit_neighborhoods:
            #solution!
            return True
        else:
            #no solution - try to expand the solution set
            for coord in set.union(*unhit_neighborhoods):
                if not any([is_manhattan_close(x, coord, k) for x in state]):
                    stack.append(state.union({coord}))
    return False

def pretty_print_tile(ones, width, height):
    for y in range(0, height):
        line = []
        for x in range(0, width):
            if (x,y) in ones:
                line.append("X")
            else:
                line.append(".")
        print "".join(line) 

tilewidth = int(argv[1])
tileheight = int(argv[2])
k = int(argv[3])

columnset = create_columns(tileheight, k)
tiles = frozenset(frozenset((0,i) for i in column) for column in columnset)
i = 1
while i < tilewidth:
    new_tiles = set()
    i += 1
    for tile in tiles:
        new_tiles.update(extend_valid(tile, columnset, i, tileheight, tilewidth, k))
    tiles = frozenset(new_tiles)

for tile in tiles:
    print "[%s]" % ",".join(str(s) for s in tile)
