'''
Advent of Code 2015 Day 20 - Infinite Elves and Infinite Houses 
'''
from math import sqrt
debug_on = False 
part_one = False

INPUT = 34_000_000

max_gifts = 0
house = 1

def fifty_factors(n):
    '''Returns the first 50 factors of a number. This is the list of 50 elves '''
    factors = []
    for i in range(1, int(n ** 0.5) + 1):
        if n % i == 0:
            if n // i <= 50:  
                factors.append(i)
            if i != n // i:
                if n // (n // i) <= 50: 
                    factors.append(n // i)
    return factors

def part_two(house: int) -> int:
    '''Returns the number of gifts a given house will get'''
    return 11 * sum(fifty_factors(house))

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
    house = 500_000
    while max_gifts < INPUT:
        gifts = part_two(house)
        if gifts > max_gifts:
            max_gifts = gifts
        house += 1    
    
    print(f"Part two: {house - 1}")