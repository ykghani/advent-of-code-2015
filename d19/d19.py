'''
Advent of Code 2015 Day 19 - Medicine for Rudolph
'''
from pathlib import Path
import itertools

script_dir = Path(__file__).parent
file_path = script_dir / 'd19_input.txt'


with open(file_path, 'r') as file: 
    lines = file.readlines()

replacements = {}
for line in lines[:-1]:
    if '=>' in line: 
        key, val = line.strip().split(' => ')
        if key in replacements:
            replacements[key].append(val)
        else:
            replacements[key] = [val]

inp = lines[-1].strip()

print(replacements)

# replacements = {'H' : ['HO', 'OH'], 'O' : ['HH']}

unique = set()
# inp = 'HOHOHO'


for start in range(len(inp)):
    for length in range(len(inp) - start + 1):
        # out = inp[: start]
        substr = inp[start: start + length]
        if substr in replacements:
            for rep in replacements[substr]:
                out =  inp[: start] + rep + inp[start + length:]
                unique.add(out)

print(f"Part one: {len(unique)}")