'''
Advent of Code 2015 Day 23 - Openiing the Turing Lock 
'''

instructions = []
file_path = 'd23_input.txt'
with open(file_path, 'r') as file: 
    for line in file: 
        line = line.strip()
        instructions.append(line.split())

vals = {'a': 1, 'b': 0}
i = 0

while True: 
    ins = instructions[i]
    if ins[0] == 'hlf':
        vals[ins[1]] /= 2
        i += 1
    elif ins[0] == 'tpl':
        vals[ins[1]] *= 3
        i += 1
    elif ins[0] == 'inc':
        vals[ins[1]] += 1 
        i += 1
    elif ins[0] == 'jmp':
        if ins[1][0] == '+':
            i += int(ins[1][1:])
        else:
            i -= int(ins[1][1:])
        continue
    elif ins[0] == 'jie':
        if vals[ins[1][0]] % 2 == 0: 
            if ins[2][0] == '+':
                i += int(ins[2][1: ])
            else: 
                i -= int(ins[2][1: ])
        else:
            i += 1
    elif ins[0] == 'jio':
        if vals[ins[1][0]] == 1:
            if ins[2][0] == '+':
                i += int(ins[2][1: ])
            else:
                i -= int(ins[2][1: ])
        else:
            i += 1
    
    if i < 0 or i > len(instructions) - 1: 
        break 

print(f"Part 1 -- a: {vals['a']} b: {vals['b']}")
    