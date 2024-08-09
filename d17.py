'''
AOC 2015 Day 17 - No Such Thing As Too Much 
'''
import itertools
AMOUNT_OF_NOG = 150 
containers = sorted([50, 44, 11, 49, 42, 46, 18, 32, 26, 40, 21, 7, 18, 43, 10, 47, 36, 24, 22, 40])

count = 0
min_containers = len(containers)

for i in range(2, len(containers) + 1):
    combos = list(itertools.combinations(containers, i))
    for combo in combos:
        if sum(combo) == AMOUNT_OF_NOG: 
            count += 1
            if len(combo) < min_containers:
                min_containers = len(combo)
    
print(f"Part 1 answer: {count}")

#Part 2 
part_two = 0
combos = list(itertools.combinations(containers, min_containers))
for combo in combos:
    if sum(combo) == AMOUNT_OF_NOG: 
        part_two += 1

print(f"Part 2 answer is: {part_two}")