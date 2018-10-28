from sys import argv
from scipy.misc import comb

#usage: python problemgen.py bitcount first amount exclusionfile
#outputs rows of all bitcount -bit problems starting from first and at most amount problems

exclusionset = {}

# bit numbers for subproblems (0 == least significant)
# 0 = 00001
# 1 = 00010
# 2 = 00011
# 3 = 00100
# 4 = 00101
# 5 = 00110
# 6 = 00111
# 7 = 01000
# 8 = 01001
# 9 = 01010
#10 = 01011
#11 = 01100
#12 = 01101
#13 = 01110
#14 = 01111
#15 = 10000
#16 = 10001
#etc

#first bit is center, then N, E; S, W

#optimizations:
#1) Culling of trivials. No need to produce any problem where bits 30 or 31 are 1
#2) Non-canonical culling: No need to solve non-canonical problems
#3) Superset culling: No need to produce a problem if its subset is solved

#implementations:
#1) simple, just iterate bits from 0-29
#2) for each number, only generate problem if bits 0-14 & bits 15-29 == bits 15-29
#3) various possibilities: maybe accept initial subproblem as input?


#input: number of the problem
#output: tuple ('center', {neighborhood dict})
def int_to_tile(code):
    code += 1
    center = '0'
    neighborhood = {'N': '0', 'E': '0', 'S': '0', 'W': '0'}
    if code & 16 != 0:
        center = '1'
    if code & 8 != 0:
        neighborhood['N'] = '1'
    if code & 4 != 0:
        neighborhood['E'] = '1'
    if code & 2 != 0:
        neighborhood['S'] = '1'
    if code & 1 != 0:
        neighborhood['W'] = '1'
    return (center, neighborhood)

#input: 32 bit integer
#output: list of tuples representing the problem
#each bit represents a subproblem
def int_to_problem(code):
    ret = []
    for i in range(0, 32):
        if code & (2**i) != 0:
            ret.append(int_to_tile(i))
    return ret

def problem_to_int(problem):
    code = 0
    for tile in problem:
        tilecode = 0
        if tile[1]['W'] == '1':
            tilecode |= 1
        if tile[1]['S'] == '1':
            tilecode |= 2
        if tile[1]['E'] == '1':
            tilecode |= 4
        if tile[1]['N'] == '1':
            tilecode |= 8
        if tile[0] == '1':
            tilecode |= 16
        code |= (2**(tilecode-1))
    return code


#returns whether the code corresponds to the canonical version of the problem
def is_canonical(code):
    baseproblem = int_to_problem(code)
    mirrors = [baseproblem,
            transform(baseproblem, horizontal_mirror), 
            transform(baseproblem, vertical_mirror),
            transform(transform(baseproblem, vertical_mirror), horizontal_mirror)]
    for mirror in mirrors:
        inverse = transform(mirror, invert)
        if code > problem_to_int(inverse):
            return False
        for problem in [mirror, inverse]:
            rotations = map(lambda x: rotate_tile(x), problem)
            firstrot = [i[0] for i in rotations]
            secondrot = [i[1] for i in rotations]
            thirdrot = [i[2] for i in rotations]
            if (code > problem_to_int(firstrot)
                or code > problem_to_int(secondrot)
                or code > problem_to_int(thirdrot)):
                return False
    return True
            

#returns a new tile rotated 90 degrees clockwise
def rotate_tile(tile):
    ret = []
    rotations = 3
    while rotations > 0:
        newtile = (tile[0], {
            'N': tile[1]['W'],
            'E': tile[1]['N'],
            'S': tile[1]['E'],
            'W': tile[1]['S']})
        ret.append(newtile)
        rotations -= 1
        tile = newtile
    return ret 

def horizontal_mirror(tile):
    return (tile[0], {
        'N': tile[1]['S'],
        'E': tile[1]['E'],
        'S': tile[1]['N'],
        'W': tile[1]['W']})

def vertical_mirror(tile):
    return (tile[0], {
        'N':tile[1]['N'],
        'E':tile[1]['W'],
        'S':tile[1]['S'],
        'W':tile[1]['E']})

def invert(tile):
    return (str(1 - int(tile[0])),{
            'N': str(1 - int(tile[1]['N'])),
            'E': str(1 - int(tile[1]['E'])),
            'S': str(1 - int(tile[1]['S'])),
            'W': str(1 - int(tile[1]['W']))})

def transform(prob, func):
    return [i for i in map(func, prob)]


def is_excluded(code):
    for exclusion in exclusionset:
        if exclusion & code == exclusion:
            return True
    return False

#returns nth positive integer with k 1-bits
def get_nth_problem(n, k):
    ret = 0
    for i in reversed(range(0,30)):
        if n > comb(i, k):
            n -= comb(i, k)
            k -= 1
            ret |= 2 ** i
    return ret

def main():
    bitcount = int(argv[1])
    first = int(argv[2])
    amount = int(argv[3])
    if (len(argv) > 4):
        with open(argv[4]) as exclusionfile:
            for line in exclusionfile:
                exclusionset.add(int(line))
    foundproblems = 0
    for i in range(first, int(comb(30, bitcount))):
        problem = get_nth_problem(i, bitcount)
        if is_canonical(problem):
            if not is_excluded(problem):
                print int_to_problem(problem)
                foundproblems += 1
                if foundproblems >= amount:
                    break

if __name__ == '__main__':
    main()
