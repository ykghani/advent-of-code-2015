'''
Advent of Code 2015 Day 21 - RPG Simulator 20XX
'''
import itertools
from math import ceil

boss = {'hp': 109, 'damage': 8, 'armor': 2}
us = {'hp': 100, 'damage': 0, 'armor': 0}

#Cost, damage, armor
weapons = [(8, 4, 0), (10, 5, 0), (25, 6, 0), (40, 7, 0), (74, 8, 0)]
armor = [(13, 0, 1), (31, 0, 2), (53, 0, 3), (75, 0, 4), (102, 0, 5)]
rings = [(25, 1, 0), (50, 2, 0), (100, 3, 0), (20, 0, 1), (40, 0, 2), (80, 0, 3)]

all_rings_combos = rings + list(itertools.combinations(rings, 2))

def will_defeat_boss(boss, us):
    if us['damage'] is None or us['damage'] == 0:
        us['damage'] = 1 
        
    boss_dmg_per_turn = max(boss['damage'] - us['armor'], 1)
    us_dmg_per_turn = max(us['damage'] - boss['armor'], 1)
    
    return ceil(boss['hp'] / us_dmg_per_turn) <= ceil(us['hp'] / boss_dmg_per_turn)
    
    if us['armor'] is None or us['armor'] == 0:  
        return us['damage'] / boss['armor'] >= (boss['hp'] / us['hp']) * boss['damage']
    else:
        return us['damage'] / boss['armor'] >= (boss['hp'] / us['hp']) * boss['damage'] / us['armor']

test_boss = {'hp': 12, 'damage': 7, 'armor': 2}
test_self = {'hp': 8, 'damage': 5, 'armor': 5}

print(will_defeat_boss(test_boss, test_self))

min_cost =10 ** 6
max_cost = 0


for wep in weapons: 
    cost = wep[0]
    us['damage'] = wep[1]
    if will_defeat_boss(boss.copy(), us.copy()): 
        if cost < min_cost: 
            min_cost = cost
    else: 
        if cost > max_cost:
            max_cost = cost
            

print(f"Just weapons winning min cost: {min_cost}")
print(f"Just weapons max losing cost: {max_cost}")

for wep in weapons: 
    for arm in armor:
        us['damage'] = wep[1]
        cost = wep[0] + arm[0] 
        us['armor'] = arm[2]
        
        if will_defeat_boss(boss.copy(), us.copy()): 
            if cost < min_cost:
                min_cost = cost
        else:
            if cost > max_cost:
                max_cost = cost

print(f"Weapons and armor winning min cost: {min_cost}")
print(f"Weapons and armor losing max cost: {max_cost}")

for wep in weapons: 
    for rings in all_rings_combos:
        
        us['damage'] = wep[1]
        cost = wep[0]
        
        if len(rings) == 3:
            cost += rings[0]
            us['damage'] += rings[1]
            us['armor'] = rings[2]
        else:
            cost += rings[0][0] + rings[1][0]
            us['damage'] += rings[0][1] + rings[1][1]
            us['armor'] = rings[0][2] + rings[1][2]
        
        if will_defeat_boss(boss.copy(), us.copy()): 
            if cost < min_cost:
                min_cost = cost
        else:
            if cost > max_cost:
                max_cost = cost

print(f"Weapons and rings winning min cost: {min_cost}")
print(f"Weapons and rings losing max cost: {max_cost}")

for wep in weapons:
    for arm in armor: 
        for ring in all_rings_combos:
            if len(ring) == 3:
                cost = wep[0] + arm[0] + ring[0]
                us['damage'] = wep[1] + ring[1]
                us['armor'] = arm[2] + ring[2]
            else:
                cost = wep[0] + arm[0] + ring[0][0] + ring[1][0]
                us['damage'] = wep[1] + ring[0][1] + ring[1][1]
                us['armor'] = arm[2] + ring[0][2] + ring[1][2]
            
            if will_defeat_boss(boss.copy(), us.copy()):
                if cost < min_cost:
                    min_cost = cost
            else:
                if cost > max_cost:
                    max_cost = cost

print(f"Fully kitted winning min cost: {min_cost}")
print(f"Fully kitted losing max cost: {max_cost}")