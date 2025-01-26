'''
Advent of Code 2015 Day 22 - Wizard Simulator 20XX 
STRATEGY - try random spell selections across 500 battles and see which ones win and use the least mana? 
'''
from random import randint
from copy import deepcopy

boss = {'hp': 51, 'dmg': 9}
player = {'hp': 50, 'mana': 500, 'armor': 0}


#Spells 
magic_missile = {'mana': 53, 'dmg': 4}
drain = {'mana': 73, 'dmg': 2, 'heal': 2}

#Effects
shield = {'name': 'shield', 'mana': 113, 'armor': 7, 'turns': 6}
poison = {'name': 'poison', 'mana': 173, 'dmg': 3, 'turns': 6}
recharge = {'name': 'recharge', 'mana': 229, 'turns': 5, 'restore': 101}
spells = [magic_missile, drain, shield, poison, recharge]


def apply_effects(state):
    '''Applies all active effects and reduces their durations'''
    player = state['player']
    boss = state['boss']
    effects = state['effects']
    
    player['armor'] = 0
    
    for effect in effects[:]:
        if effect['turns'] > 0:
            if effect['name'] == 'shield':
                player['armor'] = effect['armor']
            elif effect['name'] == 'poison':
                boss['hp'] -= effect['dmg']
            elif effect['name'] == 'recharge':
                player['mana'] += effect['restore']
            effect['turns'] -= 1
        
        if effect['turns'] <= 0:
            effects.remove(effect)

def can_cast_spell(spell, state) -> bool:
    '''Check if spell can be cast based on current state'''
    if spell['mana'] > state['player']['mana']:
        return False
    if 'name' in spell:
        return not any(e['name'] == spell['name'] for e in state['effects'])
    return True

def apply_spell(spell, state):
    '''Applies spells immediate effects and adds any active effects'''
    player = state['player']
    boss = state['boss']

    player['mana'] -= spell['mana']

    if spell == magic_missile:
        boss['hp'] -= spell['dmg']
    elif spell == drain:
        boss['hp'] -= spell['dmg']
        player['hp'] += spell['heal']
    else:
        new_effect = spell.copy()
        state['effects'].append(new_effect)

def boss_turn(state):
    """Handle the boss's turn"""
    player = state['player']
    boss = state['boss']
    damage = max(1, boss['dmg'] - player['armor'])
    player['hp'] -= damage

def find_min_mana(state, total_mana=0, min_mana_found=float('inf'), part_two= False ):
    """Find minimum mana required to win using DFS"""
    # Return if we've already used more mana than the best solution
    if total_mana >= min_mana_found:
        return float('inf')
    
    if part_two:
        state['player']['hp'] -= 1
    if state['player']['hp'] <= 0:
        return float('inf')
    apply_effects(state)
    
    if state['boss']['hp'] <= 0:
        return total_mana
    
    if state['player']['hp'] <= 0 or state['player']['mana'] <= 0:
        return float('inf')
    
    for spell in spells:
        if can_cast_spell(spell, state):
            new_state = deepcopy(state)
            
            apply_spell(spell, new_state)
            new_total_mana = total_mana + spell['mana']
            
            if new_state['boss']['hp'] <= 0:
                min_mana_found = min(min_mana_found, new_total_mana)
                continue
            
            # Boss turn
            apply_effects(new_state)
            
            if new_state['boss']['hp'] <= 0:
                min_mana_found = min(min_mana_found, new_total_mana)
                continue
            
            boss_turn(new_state)
            result = find_min_mana(new_state, new_total_mana, min_mana_found, part_two)
            min_mana_found = min(min_mana_found, result)
    
    return min_mana_found

initial_state = {
    'player': deepcopy(player),
    'boss': deepcopy(boss),
    'effects': []
}

answer = find_min_mana(initial_state, part_two= True)

print(f"ANSWER: {answer}")