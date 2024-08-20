'''
Advent of Code 2015 Day 19 - Medicine for Rudolph
'''

import itertools

file_path = 'd19_input.txt'

# with open(file_path, 'r') as file: 
#     lines = file.readlines()


replacements = {'H' : ['HO', 'OH'], 'O' : ['HH']}

# replacements = {}
# for line in lines[:-1]:
#     if '=>' in line: 
#         key, val = line.strip().split(' => ')
#         if key in replacements:
#             replacements[key].append(val)
#         else:
#             replacements[key] = [val]

# inp = lines[-1].strip()

unique = set()
inp = 'HOH'

for sub in range(1, len(inp)):
    for i in range(0, len(inp), sub):
        if inp[i: sub] in replacements:
            for val in replacements[inp[i: sub]]:
                out = ''
                out += replacements[val]
                out += inp[sub: ]
                inp.add(out)

print(unique)
print(f"Part 1 answer: {len(unique)}")
            
    
