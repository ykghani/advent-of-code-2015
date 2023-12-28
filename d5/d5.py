#AOC 2015 - Day 5: https://adventofcode.com/2015/day/5

''' 
--- Day 5: Doesn't He Have Intern-Elves For This? ---

Santa needs help figuring out which strings in his text file are naughty or nice.

A nice string is one with all of the following properties:

It contains at least three vowels (aeiou only), like aei, xazegov, or aeiouaeiouaeiou.
It contains at least one letter that appears twice in a row, like xx, abcdde (dd), or aabbccdd (aa, bb, cc, or dd).
It does not contain the strings ab, cd, pq, or xy, even if they are part of one of the other requirements.
For example:

ugknbfddgicrmopn is nice because it has at least three vowels (u...i...o...), a double letter (...dd...), and none of the disallowed substrings.
aaa is nice because it has at least three vowels and a double letter, even though the letters used by different rules overlap.
jchzalrnumimnmhp is naughty because it has no double letter.
haegwjzuvuyypxyu is naughty because it contains the string xy.
dvszwmarrgswjxmb is naughty because it contains only one vowel.
How many strings are nice?

--- Part Two ---

Realizing the error of his ways, Santa has switched to a better model of determining whether a string is naughty or nice. None of the old rules apply, as they are all clearly ridiculous.

Now, a nice string is one with all of the following properties:

It contains a pair of any two letters that appears at least twice in the string without overlapping, like xyxy (xy) or aabcdefgaa (aa), but not like aaa (aa, but it overlaps).
It contains at least one letter which repeats with exactly one letter between them, like xyx, abcdefeghi (efe), or even aaa.
For example:

qjhvhtzxzqqjkmpb is nice because is has a pair that appears twice (qj) and a letter that repeats with exactly one letter between them (zxz).
xxyxx is nice because it has a pair that appears twice and a letter that repeats with one between, even though the letters used by each rule overlap.
uurcxstgmygtbstg is naughty because it has a pair (tg) but no repeat with a single letter between them.
ieodomkazucvgmuy is naughty because it has a repeating letter with one between (odo), but no pair that appears twice.
How many strings are nice under these new rules? '''

import re

file_path = './d5/d5_input.txt'

def part_one_evaluate_string(inp):
    
    cond1, cond2, cond3 = False, False, False 
    
    bad_strings = ['ab', 'cd', 'pq', 'xy']
    vowels = ['a', 'e', 'i', 'o', 'u']
    doubles = ['aa', 'bb', 'cc', 'dd', 'ee', 'ff', 'gg', 'hh', 'ii', 'jj', 'kk', 'll', 'mm', 'nn',
               'oo', 'pp', 'qq', 'rr', 'ss', 'tt', 'uu', 'vv', 'ww', 'xx', 'yy', 'zz']
    
    if any(string in inp for string in bad_strings):
        return False
    else:
        cond3 = True 
    
    vol_count = 0
    for vow in vowels:
        vol_count += inp.count(vow)
    
    if vol_count >= 3:
        cond1 = True
    else:
        cond1 = False
    
    if any(string in inp for string in doubles):
        cond2 = True
    else:
        cond2 = False 
    
    return cond1 and cond2 and cond3

def part_two_eval(inp, pattern1, pattern2):
    return pattern1.search(inp) and pattern2.search(inp)
    
    

nice_count_one, nice_count_two = 0, 0
part2_cond1_pattern = re.compile(r'(\w{2}).*?\1')
part2_cond2_pattern = re.compile(r'(\w)\w\1')

with open(file_path, 'r') as file: 
    for line in file: 
        line = line.strip()
        if part_one_evaluate_string(line):
            nice_count_one += 1

        if part_two_eval(line, part2_cond1_pattern, part2_cond2_pattern):
            nice_count_two += 1
            
file.close()

print(f'Part one answer is: {nice_count_one}')
print(f'Part two answer is: {nice_count_two}')