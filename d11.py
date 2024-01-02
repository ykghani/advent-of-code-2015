#AOC 2015 - Day 11
'''
--- Day 11: Corporate Policy ---

Santa's previous password expired, and he needs help choosing a new one.

To help him remember his new password after the old one expires, Santa has devised a method of coming up with a password based on the previous one. Corporate policy dictates that passwords must be exactly eight lowercase letters (for security reasons), so he finds his new password by incrementing his old password string repeatedly until it is valid.

Incrementing is just like counting with numbers: xx, xy, xz, ya, yb, and so on. Increase the rightmost letter one step; if it was z, it wraps around to a, and repeat with the next letter to the left until one doesn't wrap around.

Unfortunately for Santa, a new Security-Elf recently started, and he has imposed some additional password requirements:

Passwords must include one increasing straight of at least three letters, like abc, bcd, cde, and so on, up to xyz. They cannot skip letters; abd doesn't count.
Passwords may not contain the letters i, o, or l, as these letters can be mistaken for other characters and are therefore confusing.
Passwords must contain at least two different, non-overlapping pairs of letters, like aa, bb, or zz.
For example:

hijklmmn meets the first requirement (because it contains the straight hij) but fails the second requirement requirement (because it contains i and l).
abbceffg meets the third requirement (because it repeats bb and ff) but fails the first requirement.
abbcegjk fails the third requirement, because it only has one double letter (bb).
The next password after abcdefgh is abcdffaa.
The next password after ghijklmn is ghjaabcc, because you eventually skip all the passwords that start with ghi..., since i is not allowed.
Given Santa's current password (your puzzle input), what should his next password be?
'''

import re

INPUT = 'cqjxjnds'

def next_char(char): 
    ascii_val = ord(char)
    overflow = False
    
    if ascii_val >= 122: #ascii value for 'z'
        ascii_val = 97
        overflow = True
    else:
        ascii_val += 1
        
    return chr(ascii_val), overflow

def is_valid_password(password):
    password = str(password)
    cond1_pattern = r'(?:abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)'
    cond2_pattern = r'(?:aa|bb|cc|dd|ee|ff|gg|hh|ii|jj|kk|ll|mm|nn|oo|pp|qq|rr|ss|tt|uu|vv|ww|xx|yy|zz)'
    
    cond1 = re.compile(cond1_pattern)
    cond2 = re.compile(cond2_pattern)
    
    match1 = cond1.search(password)
    if match1 is None:
        match1 = False
    match2 = cond2.findall(password)
    if match2 is None or len(match2) < 2:
        match2 = False
    cond3 = any(char in password for char in {'i', 'o', 'l'})
    
    return match1 and match2 and not cond3 


def next_password(password):
    pass_len = len(password)
    password = list(password)
    
    new_char, overflow = next_char(password[pass_len - 1])
    password[pass_len - 1] = new_char
    
    ind = pass_len - 2
    while overflow:

        if ind < 0:
            ind = pass_len - 1
        
        new_char, overflow = next_char(password[ind])
        password[ind] = new_char
        ind -= 1
    
    return ''.join(password)

def update_password(old_password):
    new_password = old_password
    valid_password = is_valid_password(old_password)
    iteration = 1
    
    while not valid_password: 
        new_password = next_password(new_password)
        valid_password = is_valid_password(new_password)
        iteration += 1
    
    return new_password

part_one_password = update_password(INPUT)
print(f'Part 1: {part_one_password}')

part_two_input = part_one_password[: - 3] + 'zaa' 
print(f'Input for part 2 is: {part_two_input}')

part_two_password = update_password(part_two_input)
print(f'Part 2: {part_two_password}')