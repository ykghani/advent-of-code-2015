#AOC 2015 - Day 8: https://adventofcode.com/2015/day/8
from pathlib import Path

script_dir = Path(__file__).parent
file_path = script_dir / 'd8_input.txt'

def count_string_diff(line):
    content = line[1:-1]
    code_len = len(line)
    content_len = 0
    i = 0
    
    while i < len(content):
        if content[i] == '\\':  # Found an escape sequence
            if i + 1 >= len(content):
                break
                
            if content[i + 1] == '\\' or content[i + 1] == '"':
                content_len += 1
                i += 2
            elif content[i + 1] == 'x' and i + 3 < len(content):
                content_len += 1
                i += 4
            else:
                content_len += 2
                i += 2
        else:
            content_len += 1
            i += 1
            
    return code_len - content_len

def encode_string(line):
    encoded = '"'

    for char in line:
        if char == '"':  
            encoded += '\\"'
        elif char == '\\':  
            encoded += '\\\\'
        else:  
            encoded += char
            
    # Add closing quote
    encoded += '"'
    return encoded


part_one, part_two = 0, 0
with open(file_path, 'r') as file:
    for line in file:
        line = line.strip()
        part_one += count_string_diff(line)
        part_two += len(encode_string(line)) - len(line)
        

print(part_one)
print(part_two)