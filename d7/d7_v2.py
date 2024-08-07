'''
Advent of Code 2015 Day 7 - Some Assembly Required
'''
from collections import defaultdict


wires = defaultdict(lambda: None)
assigned = set()
instructions = []
unassigned, single_gates, double_gates = [], [], []

def parse_line(line):
    if len(line) == 3: #Assignment
        key, val = line[2], line[0]
        try: 
            wires[key] = int(val)
            assigned.add(key)
        except ValueError: 
            if wires[val] is not None:
                wires[key] = wires[val]
                assigned.add(key)
            else:
                # unassigned.append((key, val))
                unassigned.append(line)

    elif len(line) == 4: #Negations
        type = 'NOT'
        if wires[line[1]] is not None: 
            if ~wires[line[1]] < 0: 
                wires[line[3]] = ~wires[line[1]] + 65536
            else:
                wires[line[3]] = ~wires[line[1]]
            assigned.add(line[3])
        else:
            # single_gates.add((type, line[0], line[3]))
            single_gates.append(line)
    
    else: 
        if 'LSHIFT' in line or 'RSHIFT' in line: 
            if wires[line[0]] is not None: 
                if line[1] == 'LSHIFT':
                    wires[line[4]] = wires[line[0]] << int(line[2])
                else:
                    wires[line[4]] = wires[line[0]] >> int(line[2])
                assigned.add(line[4])
            else:
                if line[1] == 'LSHIFT':
                    # single_gates.append(('LSHIFT', line[0], line[2]))
                    single_gates.append(line)
                else:
                    # single_gates.append(('RSHIFT', line[0], line[2]))
                    single_gates.append(line)
        else:
            if line[1] == 'AND':
                if line[0].isdigit():
                    if wires[line[2]] is not None:
                        wires[line[4]] = int(line[0]) & wires[line[2]]
                        assigned.add(line[4])
                    else:
                        double_gates.append(line)
                elif wires[line[0]] is not None and wires[line[2]] is not None:
                    wires[line[4]] = wires[line[0]] & wires[line[2]]
                    assigned.add(line[4])
                else:
                    double_gates.append(line)
            else:
                if wires[line[0]] is not None and wires[line[2]] is not None:
                    wires[line[4]] = wires[line[0]] | wires[line[2]]
                    assigned.add(line[4])
                else:
                    double_gates.append(line)
                        
    return 


# file_path = 'd7_test_input.txt'
file_path = 'd7_input.txt'
with open(file_path, 'r') as file:
    for line in file: 
        line = line.strip()
        instructions.append(line)
        
        line = line.split()
        parse_line(line)

print(f"Initial parsing complete. {len(assigned)} wires assigned")
print(f"Unassinged: {len(unassigned)}   Single Gates: {len(single_gates)}     Double Gates: {len(double_gates)}")
# print(wires)

emulate = True
i = 1
while emulate:
    
    unassigned_copy = unassigned.copy()
    
    for line in unassigned_copy:
        if line[0] in assigned:
            parse_line(line)
            unassigned.remove(line)
     
    print(f"Pass {i} of Unassigned... complete")
     
    single_gates_copy = single_gates.copy()
    for line in single_gates_copy: 
        if len(line) == 4: 
            if line[1] in assigned: 
                parse_line(line)
                single_gates.remove(line)
        else:
            if line[0] in assigned:
                parse_line(line)
                single_gates.remove(line)
    
    print(f"Pass {i} of single gates... complete")
    
    double_gates_copy = double_gates.copy()
    
    for line in double_gates_copy:
        if line[0] in assigned and line[2] in assigned: 
            parse_line(line)
            double_gates.remove(line)
        elif line[0].isdigit() and line[2] in assigned:
            parse_line(line)
            double_gates.remove(line)
        
    print(f"Pass {i} complete. Unassigned: {len(unassigned)}  Single Gates: {len(single_gates)}  Double: {len(double_gates)}")
    i += 1
    
    if len(unassigned) == 0 and len(single_gates) == 0 and len(double_gates) == 0:
        emulate = False
    
print(f"Part 1 answer is: {wires['a']}")

#Part 2
a_sig = wires['a']
overrides = [x for x in instructions if not x.endswith(' b')]
overrides.append(str(a_sig) + ' -> b')


wires = defaultdict(lambda: None)
assigned = set()
unassigned, single_gates, double_gates = [], [], []

for ins in overrides: 
    parse_line(ins.split())

emulate = True
i = 1
while emulate:
    
    unassigned_copy = unassigned.copy()
    
    for line in unassigned_copy:
        if line[0] in assigned:
            parse_line(line)
            unassigned.remove(line)
     
    print(f"Pass {i} of Unassigned... complete")
     
    single_gates_copy = single_gates.copy()
    for line in single_gates_copy: 
        if len(line) == 4: 
            if line[1] in assigned: 
                parse_line(line)
                single_gates.remove(line)
        else:
            if line[0] in assigned:
                parse_line(line)
                single_gates.remove(line)
    
    print(f"Pass {i} of single gates... complete")
    
    double_gates_copy = double_gates.copy()
    
    for line in double_gates_copy:
        if line[0] in assigned and line[2] in assigned: 
            parse_line(line)
            double_gates.remove(line)
        elif line[0].isdigit() and line[2] in assigned:
            parse_line(line)
            double_gates.remove(line)
        
    print(f"Pass {i} complete. Unassigned: {len(unassigned)}  Single Gates: {len(single_gates)}  Double: {len(double_gates)}")
    i += 1
    
    if len(unassigned) == 0 and len(single_gates) == 0 and len(double_gates) == 0:
        emulate = False
    
print(f"Part 2 answer is: {wires['a']}")

