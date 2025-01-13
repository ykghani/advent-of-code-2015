'''
Advent of Code 2015 Day 19 - Medicine for Rudolph
'''
from pathlib import Path
from collections import deque 

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

unique = set()
for start in range(len(inp)):
    for length in range(len(inp) - start + 1):
        # out = inp[: start]
        substr = inp[start: start + length]
        if substr in replacements:
            for rep in replacements[substr]:
                out =  inp[: start] + rep + inp[start + length:]
                unique.add(out)

print(f"Part one: {len(unique)}")

def reverse_replacements(replacements):
    '''Reverses the replacement dictionary'''
    
    reverse_dict = {}
    for key, values in replacements.items():
        for val in values: 
            if val in reverse_dict:
                reverse_dict[val].append(key)
            else:
                reverse_dict[val] = [key]
    
    return dict(sorted(reverse_dict.items(), key= lambda x: len(x[0]), reverse= True))

def find_min_steps(target, replacements):
    reverse_rep = reverse_replacements(replacements)

    queue = [(target, 0)]
    seen = {target}
    while queue:
        current, steps = queue.pop()
        
        if current == 'e':
            return steps

        for start in range(len(current)):
            for length in range(1, len(current) - start + 1):
                substr = current[start: start + length]
                if substr in reverse_rep:
                    for rep in reverse_rep[substr]:
                        out =  current[: start] + rep + current[start + length:]
                        seen.add(out)
                        queue.append((out, steps + 1))
    return None

print(f"Part two: {find_min_steps(inp, replacements)}")