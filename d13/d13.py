#AOC 2015 - Day 13 (SOLVED)
'''
--- Day 13: Knights of the Dinner Table ---

In years past, the holiday feast with your family hasn't gone so well. Not everyone gets along! This year, you resolve, will be different. You're going to find the optimal seating arrangement and avoid all those awkward conversations.

You start by writing up a list of everyone invited and the amount their happiness would increase or decrease if they were to find themselves sitting next to each other person. You have a circular table that will be just big enough to fit everyone comfortably, and so each person will have exactly two neighbors.

For example, suppose you have only four attendees planned, and you calculate their potential happiness as follows:

Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.
Then, if you seat Alice next to David, Alice would lose 2 happiness units (because David talks so much), but David would gain 46 happiness units (because Alice is such a good listener), for a total change of 44.

If you continue around the table, you could then seat Bob next to Alice (Bob gains 83, Alice gains 54). Finally, seat Carol, who sits next to Bob (Carol gains 60, Bob loses 7) and David (Carol gains 55, David gains 41). The arrangement looks like this:

     +41 +46
+55   David    -2
Carol       Alice
+60    Bob    +54
     -7  +83
After trying every other seating arrangement in this hypothetical scenario, you find that this one is the most optimal, with a total change in happiness of 330.

What is the total change in happiness for the optimal seating arrangement of the actual guest list?
'''
import re
from itertools import permutations

file_path = './d13/d13_input.txt'

pattern = re.compile(r'(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+)\.')

happiness = {'Alice' : [],
             'Bob' : [],
             'Carol' : [],
             'David' : [],
             'Eric' : [],
             'Frank' : [],
             'George' : [],
             'Mallory' : []}

with open(file_path, 'r') as file: 
    for line in file:
        line = line.strip()
        match = pattern.match(line)
        
        if match:
            name1, operation, value, name2 = match.groups()
            value = int(value) if operation == 'gain' else -int(value)

            happiness[name1].append((name2, value))

file.close()

all_permutations = permutations(happiness.keys())

max_happiness = 0
num_people = 8 
for permut in all_permutations:
    seating_score = 0
    
    for ind in range(0, num_people):
        person = permut[ind]
        
        if ind == 0:
            person_left = permut[-1]
            person_right = permut[ind + 1]
        elif ind == num_people - 1:
            person_left = permut[ind - 1]
            person_right = permut[0]
        else:
            person_left = permut[ind - 1]
            person_right = permut[ind + 1]
        
        value_left = sum([pers[1] for pers in happiness[person] if pers[0] == person_left])
        value_right = sum([pers[1] for pers in happiness[person] if pers[0] == person_right])
        
        seating_score += value_left + value_right
    
    if seating_score > max_happiness:
        max_happiness = seating_score

print(f'Part 1 answer is: {max_happiness}')            

#Part 2
max_happiness = 0 
num_people += 1
for pers in happiness: 
    happiness[person].append(('You', 0))

happiness['You'] = [('Alice', 0), ('Bob', 0), ('Carol', 0), ('David', 0), ('Eric', 0), ('Frank', 0), ('George', 0), ('Mallory', 0)]

new_permuts = permutations(happiness.keys())
for permut in new_permuts:
    seating_score = 0
    
    for ind in range(0, num_people):
        person = permut[ind]
        
        if ind == 0:
            person_left = permut[-1]
            person_right = permut[ind + 1]
        elif ind == num_people - 1:
            person_left = permut[ind - 1]
            person_right = permut[0]
        else:
            person_left = permut[ind - 1]
            person_right = permut[ind + 1]
        
        value_left = sum([pers[1] for pers in happiness[person] if pers[0] == person_left])
        value_right = sum([pers[1] for pers in happiness[person] if pers[0] == person_right])
        
        seating_score += value_left + value_right
    
    if seating_score > max_happiness:
        max_happiness = seating_score 

print(f'Part 2 answer is: {max_happiness}')
