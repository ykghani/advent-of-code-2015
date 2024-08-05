#AOC 2015 - Day 8: https://adventofcode.com/2015/day/8
import ast

file_path = '/Users/yusufghani/GitHub/advent-of-code/2015/d8/d8_input.txt'
string_literal_sum, string_memory_sum = 0, 0
ans = 0

with open(file_path, 'r') as file:
    for line in file:
        line = line.strip()
        
        # string_literal = ast.literal_eval(line)
        
        # string_memory_sum += len(string_literal)
        # string_literal_sum += len(repr(string_literal))
        ans += len(repr(line)) - len(line)
        
file.close()

# print(f"Part 1 answer is {string_literal_sum - string_memory_sum}")
print(ans)