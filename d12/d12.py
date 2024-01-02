#AOC 2015 - Day 12 (SOLVED)
'''
--- Day 12: JSAbacusFramework.io ---

Santa's Accounting-Elves need help balancing the books after a recent order. Unfortunately, their accounting software uses a peculiar storage format. That's where you come in.

They have a JSON document which contains a variety of things: arrays ([1,2,3]), objects ({"a":1, "b":2}), numbers, and strings. Your first job is to simply find all of the numbers throughout the document and add them together.

For example:

[1,2,3] and {"a":2,"b":4} both have a sum of 6.
[[[3]]] and {"a":{"b":4},"c":-1} both have a sum of 3.
{"a":[-1,1]} and [-1,{"a":1}] both have a sum of 0.
[] and {} both have a sum of 0.
You will not encounter any strings containing numbers.

What is the sum of all numbers in the document?
'''
import json

file_path = './d12/d12_input.json'


with open(file_path, 'r') as file: 
    data = json.load(file)

file.close()

def calc_json_sum(d):
    cum_sum = 0
    

    if isinstance(d, dict):
        if 'red' in d.values(): #Change needed for part 2
            return cum_sum
        else:
            for key, val in d.items():
                cum_sum += calc_json_sum(val)
    elif isinstance(d, list):
        for item in d:
            cum_sum += calc_json_sum(item)
    elif isinstance(d, (int, float)):
        cum_sum += d
    
    return cum_sum

print(calc_json_sum(data))