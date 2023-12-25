#Advent of Code 2015: https://adventofcode.com/2015/day/4

'''
--- Day 4: The Ideal Stocking Stuffer ---

Santa needs help mining some AdventCoins (very similar to bitcoins) to use as gifts for all the economically forward-thinking little girls and boys.

To do this, he needs to find MD5 hashes which, in hexadecimal, start with at least five zeroes. The input to the MD5 hash is some secret key (your puzzle input, given below) followed by a number in decimal. To mine AdventCoins, you must find Santa the lowest positive number (no leading zeroes: 1, 2, 3, ...) that produces such a hash.

For example:

If your secret key is abcdef, the answer is 609043, because the MD5 hash of abcdef609043 starts with five zeroes (000001dbbfa...), and it is the lowest such number to do so.
If your secret key is pqrstuv, the lowest number it combines with to make an MD5 hash starting with five zeroes is 1048970; that is, the MD5 hash of pqrstuv1048970 looks like 000006136ef....

--- Part Two ---

Now find one that starts with six zeroes. '''

import hashlib

inp = 'yzbqklnj'

def calculate_md5(inp):
    
    md5_hash = hashlib.md5()
    md5_hash.update(inp.encode('utf-8'))
    
    return md5_hash.hexdigest()

def part_one(inp):
    start_val = 0
    hash = str(inp) + str(start_val)
    md5_hash = calculate_md5(hash)
    
    while str(md5_hash)[0:5] != '00000':
        start_val += 1
        hash = str(inp) + str(start_val)
        md5_hash = calculate_md5(hash)
    
    return(start_val)

def part_two(inp):
    start_val = 0
    hash = str(inp) + str(start_val)
    md5_hash = calculate_md5(hash)
    prefix = '000000'
    
    while not md5_hash.startswith(prefix):
        start_val += 1
        hash = str(inp) + str(start_val)
        md5_hash = calculate_md5(hash)
    
    return start_val

print(f'Part one answer is: {part_one(inp)}')
print(f'Part two answer is: {part_two(inp)}')
