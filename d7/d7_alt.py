#AOC 2015 - Day 7 ALTERNATE https://adventofcode.com/2015/day/7
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
import networkx as nx
import matplotlib.pyplot as plt

BIT_LIM = 65535

file_path = './d7/d7_input.txt'
test_file_path = './d7/d7_test_input.txt'

pattern = re.compile(
    r'(?:(?P<SIGNAL_ASSIGN_VALUE>\d+) -> (?P<SIGNAL_ASSIGN_DESTINATION>\w+))|'  # Category 1: Signal assignment
    r'(?:(?P<BINARY_SOURCE1>\w+) (?P<GATE>AND|OR) (?P<BINARY_SOURCE2>\w+) -> (?P<BINARY_DESTINATION>\w+))|'  # Category 2: Binary logic gates
    r'(?:(?P<UNARY_NOT>NOT) (?P<UNARY_SOURCE>\w+) -> (?P<UNARY_DESTINATION>\w+))|'  # Category 3: Unary logic gates
    r'(?:(?P<SHIFT_SOURCE>\w+) (?P<SHIFT_TYPE>RSHIFT|LSHIFT) (?P<SHIFT_AMOUNT>\d+) -> (?P<SHIFT_DESTINATION>\w+))|'  # Category 4: Shift operations
    r'(?:(?P<ONE_AND_SIGNAL_VALUE>\d+) AND (?P<ONE_AND_SOURCE>\w+) -> (?P<ONE_AND_DESTINATION>\w+))|'  # Category 5: 1 AND operations
    r'(?:(?P<DIRECT_SIGNAL_SOURCE>\w+) -> (?P<DIRECT_SIGNAL_DESTINATION>\w+))' #Direct assignment 
)

circuit = nx.DiGraph()
circuit.add_node('start')

def add_nodes(graph, node_list):
    
    if not isinstance(node_list, list):
        node_list = [node_list]
    
    for node in node_list:
        if not graph.has_node(node):
            graph.add_node(node)
    
    return

def normalize(val):
    if val > 0:
        return val
    else:
        return val + BIT_LIM + 1

def add_signal_assignment(graph, sig, dest):
    
    add_nodes(graph, ['start', dest])
    graph.nodes[dest]['signal'] = int(sig) 
    
    graph.add_edge('start', dest)
    
    return 

def add_binary_gate(graph, source1, source2, gate, dest, identifier):
    gate_node = gate + '_' + str(identifier)

    add_nodes(graph, [source1, source2, dest, gate_node]) 
    graph.nodes[gate_node]['logic'] = gate
    
    #Add edges
    graph.add_edge(source1, gate_node)
    graph.add_edge(source2, gate_node)
    graph.add_edge(gate_node, dest)
    
    #If possible to run calc THEN DO IT
    if all(graph.nodes[node].get('signal', None) is not None for node in {source1, source2}):
        sig1, sig2 = int(graph.nodes[source1]['signal']), int(graph.nodes[source2]['signal'])
        if gate == 'AND':
            sig = normalize(sig1 & sig2)
        else:
            sig = normalize(sig1 | sig2) 
        
        graph.nodes[dest]['signal'] = sig
    
    return 

def add_unary_gate(graph, source1, has_not, dest, identifier):
    gate_node = has_not + '_' + str(identifier)
    
    add_nodes(graph, [source1, dest, gate_node])
    graph.nodes[gate_node]['logic'] = has_not
        
    #Add edges
    graph.add_edge(source1, gate_node)
    graph.add_edge(gate_node, dest)
    
    #If possible to run calc THEN DO IT
    if graph.nodes[source1].get('signal', None) is not None:
        sig = normalize(~int((graph.nodes[source1]['signal'])))
        graph.nodes[dest]['signal'] = sig
    
    return 

def add_shift_gate(graph, source1, shift, shift_amt, dest, identifier):
    shift_node = shift + '_' + str(identifier)
    
    add_nodes(graph, [source1, dest, shift_node])
    attr = {'logic' : shift, 'shift_val' : shift_amt}
    graph.nodes[shift_node].update(attr)
        
    #Add edges
    graph.add_edge(source1, shift_node)
    graph.add_edge(shift_node, dest)
    
    #Run calculation and update nodes if possible 
    if graph.nodes[source1].get('signal', None) is not None:
        if shift == 'LSHIFT':
            sig = normalize(int(graph.nodes[source1]['signal']) << int(shift_amt))
        else:
            sig = normalize(int(graph.nodes[source1]['signal']) >> int(shift_amt))
        
        graph.nodes[dest]['signal'] = sig 
        
    return 

def add_and_one(graph, signal, source1, dest, identifier):

    art_node = '1_' + str(identifier)
    
    add_nodes(graph, [source1, 'start', art_node, dest])

    graph.nodes[art_node]['signal'] = signal 
    
    #Add edges
    graph.add_edge('start', art_node)
    graph.add_edge(source1, art_node)
    graph.add_edge(art_node, dest)
    
    #Check to see if calc can be performed
    if graph.nodes[source1].get('signal', None) is not None:
        sig = normalize(int(signal) & int(graph.nodes[source1].get('signal', None)))
        graph.nodes[dest]['signal'] = sig 
    
    return 

def direct_assignment(graph, source, dest):
    
    add_nodes(graph, [source, dest])
    
    #Add edges
    graph.add_edge(source, dest)
    
    if graph.nodes[source].get('signal', None) is not None:
        sig = graph.nodes[source].get('signal')
        graph.nodes[dest]['signal'] = int(sig)

    return

def parse_str(inp_str, identifier):
    match = pattern.match(inp_str)
    
    if match:
        signal_assign_val = match.group('SIGNAL_ASSIGN_VALUE')
        signal_assign_dest = match.group('SIGNAL_ASSIGN_DESTINATION')
        bin_source1 = match.group('BINARY_SOURCE1')
        gate = match.group('GATE')
        bin_source2 = match.group('BINARY_SOURCE2')
        bin_dest = match.group('BINARY_DESTINATION')
        unu_not = match.group('UNARY_NOT')
        unu_source = match.group('UNARY_SOURCE')
        unu_dest = match.group('UNARY_DESTINATION')
        shift_source = match.group('SHIFT_SOURCE')
        shift_type = match.group('SHIFT_TYPE')
        shift_amt = match.group('SHIFT_AMOUNT')
        shift_dest = match.group('SHIFT_DESTINATION')
        one_and = match.group('ONE_AND_SIGNAL_VALUE')
        one_and_source = match.group('ONE_AND_SOURCE')
        one_and_dest = match.group('ONE_AND_DESTINATION')
        direct_sig_source = match.group('DIRECT_SIGNAL_SOURCE')
        direct_sig_dest = match.group('DIRECT_SIGNAL_DESTINATION')

    if signal_assign_val is not None and signal_assign_dest is not None:
        add_signal_assignment(circuit, sig= signal_assign_val, dest= signal_assign_dest)
    elif all(arg is not None for arg in {bin_source1, gate, bin_source2, bin_dest}):
        add_binary_gate(graph= circuit, source1= bin_source1, source2= bin_source2, gate= gate, dest= bin_dest, identifier= identifier)
    elif all(arg is not None for arg in {unu_not, unu_source, unu_dest}):
        add_unary_gate(graph= circuit, source1= unu_source, has_not= unu_not, dest= unu_dest, identifier= identifier)
    elif all(arg is not None for arg in {shift_source, shift_type, shift_amt, shift_dest}):
        add_shift_gate(graph= circuit, source1= shift_source, shift= shift_type, shift_amt= shift_amt, dest= shift_dest, identifier= identifier)
    elif all(arg is not None for arg in {one_and, one_and_source, one_and_dest}):
        add_and_one(graph= circuit, signal= one_and, source1= one_and_source, dest= one_and_dest, identifier= identifier)
    elif direct_sig_source is not None and direct_sig_dest is not None:
        pass
    else:
        raise ValueError 
    
    return

#Might need to deprecate
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

def evaluate_gate(graph, gate):
    preds = list(graph.predecessors(gate))
    gate_type = graph.nodes[gate].get('logic', None)
    
    if all(graph.nodes[pred].get('signal', None) is not None for pred in preds):
        successor = list(graph.successors(gate))[0]
        if gate_type == 'NOT':
            val = normalize(~(int(graph.nodes[preds[0]].get('signal', None))))
        elif gate_type == 'AND':
            sig1, sig2 = int(graph.nodes[preds[0]].get('signal')), int(graph.nodes[preds[1]].get('signal'))
            val = normalize(sig1 & sig2)
        elif gate_type == 'OR':
            sig1, sig2 = int(graph.nodes[preds[0]].get('signal')), int(graph.nodes[preds[1]].get('signal'))
            val = normalize(sig1 | sig2)
        elif gate_type == 'LSHIFT':
            sig = int(graph.nodes[preds[0]].get('signal'))
            shift_amt = int(graph.nodes[gate].get('shift_val', None))
            val = normalize(sig << shift_amt)
        else: #RSHIFT CASE
            sig = int(graph.nodes[preds[0]].get('signal'))
            shift_amt = int(graph.nodes[gate].get('shift_val', None))
            val = normalize(sig >> shift_amt)
        
        graph.nodes[successor]['signal'] = int(val)
            
    return

print(f'Starting file processing...')
with open(file_path, 'r') as file:
    identifier = 0
    
    for line in file:
        # print(f"Processing line: {identifier + 1}")
        line = line.strip()
        parse_str(line, identifier)
        identifier += 1

print(f'File processing... complete')       
file.close()

print(f"File processing complete. Loaded grid with {len(circuit.nodes())} nodes")

gates = [gate for gate in circuit.nodes() if circuit.nodes[gate].get('logic', None) is not None]
print(f'Gates: {gates}')

counter = 0 
while counter < 1000: 
    unprocessed_nodes = [node for node in circuit.nodes() if circuit.nodes[node].get('signal') is None and circuit.nodes[node].get('logic', None) is None]
    # signal_nodes = [node for node in circuit.nodes() if circuit.node[node].get()]
    # print(f'Unprocessed nodes: {unprocessed_nodes}')

    if len(unprocessed_nodes) == 0:
        break
    else:
        print(f"Gate processing...")
        for gate in gates:
            evaluate_gate(circuit, gate)
            print(f'Gate {gate} processing... complete.')

    counter += 1
# bfs_nodes = list(nx.bfs_tree(circuit, 'start'))

unprocessed_nodes = [node for node in circuit.nodes() if circuit.nodes[node].get('singal', None) is None and circuit.nodes[node].get('logic', None) is None]
print(f"The number of unprocessed nodes left are: {len(unprocessed_nodes)}")
#Update - iterate though all nodes until all of them have a signal value
#if node has a signal, pass over it 

# for node, data in circuit.nodes(data=True):
# for node in list(circuit.nodes):
    
# #     # calc_signal(circuit, node)
#     node_data = circuit.nodes[node]
#     print(f'Node {node}: {node_data}')


# pos = nx.spring_layout(circuit)
# nx.draw(circuit, pos, with_labels=True, font_weight='bold', node_size=50, node_color='skyblue', font_color='black', font_size=10, arrowsize=20)

# # Display edge weights
# edge_labels = nx.get_edge_attributes(circuit, ('signal', 'gate'))
# nx.draw_networkx_edge_labels(circuit, pos, edge_labels=edge_labels)

# plt.show()

print()