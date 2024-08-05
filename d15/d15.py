#AOC 2015 - Day 15
'''
--- Day 15: Science for Hungry People ---

Today, you set out on the task of perfecting your milk-dunking cookie recipe. All you have to do is find the right balance of ingredients.

Your recipe leaves room for exactly 100 teaspoons of ingredients. You make a list of the remaining ingredients you could use to finish the recipe (your puzzle input) and their properties per teaspoon:

capacity (how well it helps the cookie absorb milk)
durability (how well it keeps the cookie intact when full of milk)
flavor (how tasty it makes the cookie)
texture (how it improves the feel of the cookie)
calories (how many calories it adds to the cookie)
You can only measure ingredients in whole-teaspoon amounts accurately, and you have to be accurate so you can reproduce your results in the future. The total score of a cookie can be found by adding up each of the properties (negative totals become 0) and then multiplying together everything except calories.

For instance, suppose you have these two ingredients:

Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
Then, choosing to use 44 teaspoons of butterscotch and 56 teaspoons of cinnamon (because the amounts of each ingredient must add up to 100) would result in a cookie with the following properties:

A capacity of 44*-1 + 56*2 = 68
A durability of 44*-2 + 56*3 = 80
A flavor of 44*6 + 56*-2 = 152
A texture of 44*3 + 56*-1 = 76
Multiplying these together (68 * 80 * 152 * 76, ignoring calories for now) results in a total score of 62842880, which happens to be the best score possible given these ingredients. If any properties had produced a negative total, it would have instead become zero, causing the whole score to multiply to zero.

Given the ingredients in your kitchen and their properties, what is the total score of the highest-scoring cookie you can make?
'''

import re, itertools

TOTAL_TEASPOONS = 100

file_path = './d15/d15_input.txt'
test_file_path = './d15/d15_test_input.txt'
pattern = re.compile(r'(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)')


class Ingredient:
    
    _tsps = 0
    
    def __init__(self, name, capacity, durability, flavor, texture, calories):
        self.name = name
        self.capacity = int(capacity)
        self.durability = int(durability)
        self.flavor = int(flavor)
        self.texture = int(texture)
        self.calories = int(calories)
    
    @property
    def tsps(self):
        return self._tsps
    
    @tsps.setter
    def tsps(self, val):
        self._tsps = val
        return 
    
    def __repr__(self):
        return f'{self.name}, tsps= {self._tsps}'
    
def calc_cookies(ingredients):
    
    overall_cap, overall_dur, overall_flav, overall_text = 0, 0, 0,0
    
    for ingredient in ingredients:
        overall_cap += ingredient.capacity * ingredient.tsps
        overall_dur += ingredient.durability * ingredient.tsps
        overall_flav += ingredient.flavor * ingredient.tsps
        overall_text += ingredient.texture * ingredient.tsps
    
    if overall_cap < 0: 
        overall_cap = 0
    
    if overall_dur < 0: 
        overall_dur = 0
    
    if overall_flav < 0:
        overall_flav = 0
    
    if overall_text < 0:
        overall_text = 0
    
    return overall_cap * overall_dur * overall_flav * overall_text

def calc_calories(ingredients):
    cals = 0
    for ingredient in ingredients:
        cals += ingredient.calories * ingredient.tsps
    
    return cals

def partition(n, k, memo={}):
    if k == 0:
        return [[n]]
    if (n, k) in memo:
        return memo[(n, k)]

    result = []
    for i in range(1, n + 1):
        if i <= n - i:
            sub_partitions = partition(n - i, k - 1, memo)
            for sub_partition in sub_partitions:
                result.append([i] + sub_partition)

    memo[(n, k)] = result
    return result

ingredients = []
with open(file_path, 'r') as file: 
    for line in file: 
        match = pattern.search(line)
        
        if match:
            name, capacity, durability, flavor, texture, calories = match.groups()
            ingredients.append(Ingredient(name, capacity, durability, flavor, texture, calories))
            
file.close()

def gen_ingredient_lists(total_teaspoons, ingredients):
    result = []
    n_ingredients = len(ingredients)
    
    for alloc in itertools.product(range(total_teaspoons + 1), repeat=n_ingredients):
        if sum(alloc) == total_teaspoons:
            result.append(alloc)
    
    return result


res = gen_ingredient_lists(TOTAL_TEASPOONS, ingredients)

max_score = 0
for way in res: 
    ingredients[0].tsps = way[0]
    ingredients[1].tsps = way[1]
    ingredients[2].tsps = way[2]
    ingredients[3].tsps = way[3]
    
    score = calc_cookies(ingredients)
    if score > max_score:
        max_score = score

print(f"Part 1 answer: {max_score}")

#Part 2
CALORIE_LIMIT = 500 

part_two = 0
for way in res: 
    ingredients[0].tsps = way[0]
    ingredients[1].tsps = way[1]
    ingredients[2].tsps = way[2]
    ingredients[3].tsps = way[3]
    
    if calc_calories(ingredients) == CALORIE_LIMIT:
        score = calc_cookies(ingredients)
        if score > part_two:
            part_two = score

print(f'Part 2 answer: {part_two}')