'''
Advent of Code 2015 Day 22 - Wizard Simulator 20XX 
STRATEGY - try random spell selections across 500 battles and see which ones win and use the least mana? 
'''
from random import randint

boss = {'hp': 51, 'dmg': 9}
us = {'hp': 50, 'mana': 500, 'armor': 0}

# boss = {'hp': 14, 'dmg': 8}
# us = {'hp': 10, 'mana': 250, 'armor': 0}

min_mana_used = 10 ** 6

magic_missile = {'mana': 53, 'dmg': 4}
drain = {'mana': 73, 'dmg': 2, 'heal': 2}

#Effects
shield = {'name': 'shield', 'mana': 113, 'armor': 7, 'turns': 6 - 1}
poison = {'name': 'poison', 'mana': 173, 'dmg': 3, 'turns': 6 - 1}
recharge = {'name': 'recharge', 'mana': 229, 'turns': 5 - 1, 'restore': 101}
spells = [magic_missile, drain, shield, poison, recharge]

def apply_effects(active_effects, boss, us):
    if len(active_effects) == 0: 
        return 
    else: 
        for effect in active_effects:
            if effect['turns'] > 0: 
                if effect['mana'] == 113: #Shield
                    us['armor'] = effect['armor']
                elif effect['mana'] == 173: 
                    boss['hp'] -= effect['dmg']
                else:
                    us['mana'] += effect['restore']
                
                effect['turns'] -= 1
            # else:
            #     if effect['name'] == 'shield':
            #         us['armor'] = 0
            #     active_effects.remove(effect)
    
    for effect in active_effects: 
        if effect['turns'] == 0: 
            if effect['name'] == 'shield':
                us['armor'] = 0
            active_effects.remove(effect)
        
    return

def check_winner(boss, us): 
    if us['hp'] <= 0 or us['mana'] <= 0: 
        return 'boss'
    elif boss['hp'] <= 0:
        return 'us'
    else:
        return None 

def fight(boss, us, override = False): 
    still_fighting = True
    our_turn = True
    mana_used = 0
    active_effects = list()
    turn_count = 0 
    
    while still_fighting: 
        if our_turn: 
            
            apply_effects(active_effects, boss, us)
            if boss['hp'] <= 0:
                return mana_used
            # still_fighting = check_winner(boss, us)
            # if not still_fighting: 
            #     break 
            
            if override: 
                if turn_count == 0:
                    n = 4
                elif turn_count == 2: 
                    n = 2
                elif turn_count == 4: 
                    n = 1
                elif turn_count == 6: 
                    n = 3
                elif turn_count == 8: 
                    n = 0
            else: 
                n = randint(0, 4)
                while 'name' in spells[n] and spells[n]['name'] in [effect['name'] for effect in active_effects]:
                    n = randint(0, 4)
            # while spells[n] in active_effects: 
            #     n = randint(0, 4)
            spell_choice = spells[n]
            
            us['mana'] -= spell_choice['mana']
            if us['mana'] <= 0: 
                return None 
            mana_used += spell_choice['mana']
            
            if n == 0:
                boss['hp'] -= spell_choice['dmg']
            elif n == 1: 
                boss['hp'] -= spell_choice['dmg']
                us['hp'] += spell_choice['heal']
            else: #Effect based spells
                active_effects.append(spell_choice.copy())
                
            our_turn = False

        else:
            apply_effects(active_effects, boss, us)
            if boss['hp'] <= 0: 
                return mana_used
            # still_fighting = check_winner(boss, us)
            # if not still_fighting: 
            #     break 
            
            
            us['hp'] -= boss['dmg'] - us['armor']
            our_turn = True
        
        if us['hp'] <= 0 or us['mana'] <= 0: 
            return None 
        elif boss['hp'] <= 0: 
            return mana_used
        
        turn_count += 1
        
        print(f"----END OF TURN {turn_count}--------")
        print(f"Player stats: {us}")
        print(f"Boss stats: {boss}")

battle_count = 0
BATTLE_LIM = 10000
while battle_count < BATTLE_LIM:
    mana_used = fight(boss.copy(), us.copy(), False)
    if mana_used is not None: 
        if mana_used < min_mana_used:
            min_mana_used = mana_used
    
    battle_count += 1

print(f"Minimum mana used after {BATTLE_LIM} battles is {min_mana_used} ")
    