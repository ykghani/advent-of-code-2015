'''
Advent of Code 2015 Day 24 - It Hangs in the Balance
'''

import itertools
from functools import reduce

input = [1, 3, 5, 11, 13, 17, 19,
        23, 29, 31, 41, 43, 47,
        53, 59, 61, 67, 71, 73,
        79, 83, 89, 97, 101, 103,
        107, 109, 113]

input.sort(reverse= True)

target = sum(input) // 3 
part_two_target = sum(input) // 4 
print(f"Target weight is: {target}")

possible_configs = {}
part_two_configs = {}
for r in range(1, len(input) // 4 + 1):
    comb = itertools.combinations(input, r)
    possible_configs[r] = list()
    part_two_configs[r] = list() 
    for c in comb:
        if sum(c) == target: 
            possible_configs[r].append(c)
        
        if sum(c) == part_two_target:
            part_two_configs[r].append(c)

#Part 1
min_qe = 10 ** 20 
sixers = possible_configs[6]
for six in sixers:  
    result = reduce(lambda x, y: x * y, six)
    if result < min_qe: 
        min_qe = result

#Part 2 Answer
part_two_qe = 10 ** 50 
p2_min_pkg = min(key for key in part_two_configs.keys() if part_two_configs[key] != [])
part_two_qe = min(reduce(lambda x, y: x * y, c) for c in part_two_configs[p2_min_pkg])

print(f"Lowest QE is {min_qe}")
print(f"Part 2 answer: {part_two_qe}")