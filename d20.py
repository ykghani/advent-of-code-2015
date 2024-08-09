'''
Advent of Code 2015 Day 20 - Infinite Elves and Infinite Houses 
'''
from math import sqrt
debug_on = False 
part_one = False

INPUT = 34000000
# INPUT = 200 

max_gifts = 0
house = 1

if part_one: 
    while max_gifts < INPUT: 
        gifts = 0
        house_root = int(sqrt(house))
        for n in range(1, house_root + 1):
            if house % n == 0: 
                gifts += 10 * n
                if n != house // n:  # Avoid adding the square root twice
                    gifts += 10 * (house // n)
        
        if debug_on:
            print(f"House {house} received {gifts} total gifts")
        
        if gifts > max_gifts:
            max_gifts = gifts
        
        house += 1
        
    print(f"Part 1 answer is: {house - 1}")
else:
    while max_gifts < INPUT:
        gifts = 0
        elf_count = 0
        house_root = int(sqrt(house))
        
            
    for n in range(1, house + 1):
        if house % n == 0:  # n is a divisor of house
            if house // n <= 50:  # Check if the elf visits this house (within the first 50)
                gifts += 11 * n
        
    if gifts > max_gifts:
        max_gifts = gifts
    
        
        # while elf_count <= 50: 
        #     for n in range(1, house_root + 1):
        #         if house % n == 0: 
        #             gifts += 11 * n
        #             elf_count += 1
        #             if n != house // n:  # Avoid adding the square root twice
        #                 gifts += 11 * (house // n)
        #                 elf_count += 1
            
        # if gifts > max_gifts: 
        #     max_gifts = gifts
        
        house += 1
    
    print(f"Part 2 answer is: {house -1}")
                
#61820 is too LOW 
#123637 is too LOW 
#Part Two 

        