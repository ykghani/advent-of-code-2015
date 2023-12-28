#AOC 2015 - Day 7: https://adventofcode.com/2015/day/7
'''--- Day 7: Some Assembly Required ---

This year, Santa brought little Bobby Tables a set of wires and bitwise logic gates! Unfortunately, little Bobby is a little under the recommended age range, and he needs help assembling the circuit.

Each wire has an identifier (some lowercase letters) and can carry a 16-bit signal (a number from 0 to 65535). A signal is provided to each wire by a gate, another wire, or some specific value. Each wire can only get a signal from one source, but can provide its signal to multiple destinations. A gate provides no signal until all of its inputs have a signal.

The included instructions booklet describes how to connect the parts together: x AND y -> z means to connect wires x and y to an AND gate, and then connect its output to wire z.

For example:

123 -> x means that the signal 123 is provided to wire x.
x AND y -> z means that the bitwise AND of wire x and wire y is provided to wire z.
p LSHIFT 2 -> q means that the value from wire p is left-shifted by 2 and then provided to wire q.
NOT e -> f means that the bitwise complement of the value from wire e is provided to wire f.
Other possible gates include OR (bitwise OR) and RSHIFT (right-shift). If, for some reason, you'd like to emulate the circuit instead, almost all programming languages (for example, C, JavaScript, or Python) provide operators for these gates.

For example, here is a simple circuit:

123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
After it is run, these are the signals on the wires:

d: 72
e: 507
f: 492
g: 114
h: 65412
i: 65079
x: 123
y: 456
In little Bobby's kit's instructions booklet (provided as your puzzle input), what signal is ultimately provided to wire a? '''

import re
import pygates
import networkx as nx
import matplotlib.pyplot as plt

BIT_LIM = 65535

file_path = './d7/d7_input.txt'
test_file_path = './d7/d7_test_input.txt'
pattern = re.compile(r'(?P<source1>\w+|\d+)\s*(?P<gate>AND|OR|RSHIFT|LSHIFT|NOT)?\s*(?P<source2>\w+)?\s*->\s*(?P<destination>\w+)')

#How to handle edge cases like: 1 AND gd -> ge
def parse_str(inp_str):
    match = pattern.match(inp_str)
    signal, gate_shift = None, None

    if match:
        logic_gate = match.group('gate')
        source1 = match.group('source1')
        source2 = match.group('source2')
        destination = match.group('destination')
    else:
        raise ValueError

    if source1.isdigit():
        signal = int(source1)
        source1 = 'start'
    elif source1 == 'NOT':
        logic_gate = 'NOT'
        source1 = source2
        source2 = None
        
    if logic_gate in {'LSHIFT', 'RSHIFT'}:
        gate_shift = int(source2)
        source2 = None
    
    gate = (logic_gate, gate_shift)
    
    return source1, source2, signal, gate, destination

def evaluate_logic(gate, *vals, **kwargs):
    ans = None
    
    if gate[0] == 'NOT':
        ans = ~(vals[0][0])
    elif gate[0] == 'AND':
        ans = vals[0][0] & vals[0][1]
    elif gate[0] == 'OR':
        ans = vals[0][0] | vals[0][1]
    elif gate[0] == 'LSHIFT':
        ans = vals[0][0] << gate[1]
    elif gate[0] == 'RSHIFT':
        ans = vals[0][0] >> gate[1]
    
    if ans < 0:
        ans += BIT_LIM + 1
    
    return ans 

#Need to sequence logic of how nodes and evaluated to go from start to sink 
def calc_signal(graph, node):
    preds = list(graph.predecessors(node))    
    edges = [graph[pred][node] for pred in preds]
    gates = [edge.get('gate', None) for edge in edges] 
    signals = [edge.get('signal', None) for edge in edges]
    # signals = [graph.nodes[pred].get('signal', None) for pred in preds]
    num_edges = len(edges)
    
    
    for pred in preds:
        
        if graph.nodes[pred].get('signal', None) is None and pred != 'start':
            calc_signal(graph, pred)
                 
        if num_edges <= 1 and pred == 'start':
            new_attr = {'signal' : signals[0]}
        elif num_edges == 1 and gates[0][0] in {'NOT', 'RSHIFT', 'LSHIFT'}:
            vals = [graph.nodes[pred]['signal'] for pred in preds]
            sig = evaluate_logic(gates[0], vals)
            new_attr = {'signal' : sig}
        else: #Case where there are multiple predecessors
            # vals = [graph.nodes[pred].get('signal', None) for pred in preds] 
            sig = evaluate_logic(gates[0], signals) #MAKING THE ASSUMPTION THAT ALL OF THE GATES WILL BE THE SAME 
            new_attr = {'signal' : sig}
            
        graph.nodes[node].update(new_attr)
    
    return 

circuit = nx.DiGraph()
circuit.add_node('start')
with open(test_file_path, 'r') as file:
    for line in file:
        line = line.strip()
        source1, source2, signal, logic_gate, dest = parse_str(line)

        if source1 is not None and not circuit.has_node(source1):
            circuit.add_node(source1)
        
        if source2 is not None and not circuit.has_node(source2):
            circuit.add_node(source2)
        
        if dest is not None and not circuit.has_node(dest):
            circuit.add_node(dest)
        
        if source1 is not None and dest is not None:
            circuit.add_edge(source1, dest, gate= logic_gate, signal= signal)
        
        if source2 is not None and dest is not None: 
            circuit.add_edge(source2, dest, gate= logic_gate, signal= signal)
        
file.close()

bfs_nodes = list(nx.bfs_tree(circuit, 'start'))

# for node, data in circuit.nodes(data=True):
for node in bfs_nodes:
    calc_signal(circuit, node)
    print(f'Node {node}: {circuit.nodes[node]}')


pos = nx.spring_layout(circuit)
nx.draw(circuit, pos, with_labels=True, font_weight='bold', node_size=200, node_color='skyblue', font_color='black', font_size=10, arrowsize=20)

# Display edge weights
edge_labels = nx.get_edge_attributes(circuit, ('signa', 'gate'))
nx.draw_networkx_edge_labels(circuit, pos, edge_labels=edge_labels)

# plt.show()