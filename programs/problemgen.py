from sys import argv
from scipy.misc import comb

#usage: python problemgen.py bitcount first amount exclusionfile
#outputs rows of all bitcount -bit problems starting from first and at most amount problems

exclusionset = {}

# bit numbers for subproblems (0 == most significant)
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
#15 = 11110
#16 = 11101
#17 = 11100
#18 = 11011
#19 = 11010
#20 = 11001
#21 = 11000
#22 = 10111
#23 = 10110
#24 = 10101
#25 = 10100
#26 = 10011
#27 = 10010
#28 = 10001
#29 = 10000
#30 = 11111
#31 = 00000

#for tiles 0-14, tile+15 is the tile's inversion

#first bit is center, then N, E; S, W

#optimizations:
#1) Culling of trivials. No need to produce any problem where bits 30 or 31 are 1
#2) Mirror universe culling: No need to produce problems where bits 0-14 are a PROPER superset of 15-29
#3) Superset culling: No need to produce a problem if its subset is solved

#implementations:
#1) simple, just iterate bits from 0-29
#2) for each number, only generate problem if bits 0-14 & bits 15-29 == bits 15-29
#3) various possibilities: maybe accept initial subproblem as input?


#input: number of the problem
#output: tuple ('center', {neighborhood dict})
def int_to_tile(code):
    center = '1'
    neighborhood = {'N': '1', 'E': '1', 'S': '1', 'W': '1'}
    code = (30 - code) & 31
    if code & 16 != 0:
        center = '0'
    else:
        code = (code - 1) ^ 0b1111
    if code & 8 != 0:
        neighborhood['N'] = '0'
    if code & 4 != 0:
        neighborhood['E'] = '0'
    if code & 2 != 0:
        neighborhood['S'] = '0'
    if code & 1 != 0:
        neighborhood['W'] = '0'
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

def is_mirror_universe(code):
    return (code >> 15) & (code & 32767) == code & 32767 && code >> 15 != code & 32767

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
    for i in range(first, first+amount):
        problem = get_nth_problem(i, bitcount)
        if not is_mirror_universe(problem):
            if not is_excluded(problem):
                print int_to_problem(problem)

if __name__ == '__main__':
    main()
