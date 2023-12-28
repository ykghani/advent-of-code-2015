#AOC 2015 - DAY 9: https://adventofcode.com/2015/day/9
'''
--- Day 9: All in a Single Night ---

Every year, Santa manages to deliver all of his presents in a single night.

This year, however, he has some new locations to visit; his elves have provided him the distances between every pair of locations. He can start and end at any two (different) locations he wants, but he must visit each location exactly once. What is the shortest distance he can travel to achieve this?

For example, given the following distances:

London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
The possible routes are therefore:

Dublin -> London -> Belfast = 982
London -> Dublin -> Belfast = 605
London -> Belfast -> Dublin = 659
Dublin -> Belfast -> London = 659
Belfast -> Dublin -> London = 605
Belfast -> London -> Dublin = 982
The shortest of these is London -> Dublin -> Belfast = 605, and so the answer is 605 in this example.

What is the distance of the shortest route?
'''
from collections import defaultdict
from itertools import permutations

file_path = './d9/d9_input.txt'
test_file_path = './d9/d9_test_input.txt'

locs = set()
routes = defaultdict(dict)

with open(file_path, 'r') as file:
    for line in file: 
        line = line.strip().split()
        source, dest, dist = line[0], line[2], int(line[-1])
        
        locs.add(source)
        locs.add(dest)
        
        routes[source][dest] = dist
        routes[dest][source] = dist
        
    print(f'Graph initialization and loading... complete')
    
file.close()

distances = list()
for path in permutations(locs):
    distance = sum(map(lambda x, y: routes[x][y], path[: -1], path[1: ]))
    distances.append(distance)
    
print(f'The answer to part 1 is: {min(distances)}')
print(f'The answer to parth 2 is: {max(distances)}')