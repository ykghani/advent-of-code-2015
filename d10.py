#AOC 2015 - Day 10
'''
--- Day 10: Elves Look, Elves Say ---

Today, the Elves are playing a game called look-and-say. They take turns making sequences by reading aloud the previous sequence and using that reading as the next sequence. For example, 211 is read as "one two, two ones", which becomes 1221 (1 2, 2 1s).

Look-and-say sequences are generated iteratively, using the previous value as input for the next step. For each step, take the previous value, and replace each run of digits (like 111) with the number of digits (3) followed by the digit itself (1).

For example:

1 becomes 11 (1 copy of digit 1).
11 becomes 21 (2 copies of digit 1).
21 becomes 1211 (one 2 followed by one 1).
1211 becomes 111221 (one 1, one 2, and two 1s).
111221 becomes 312211 (three 1s, two 2s, and one 1).
Starting with the digits in your puzzle input, apply this process 40 times. What is the length of the result?
'''

INPUT = 1321131112

def next_look_and_say(val):
    val = str(val)
    ans_str, val_dict = '', dict()
    
    uniq_vals = set(val)
    
    
    
    i = 0
    while i < len(val):
    # for i in range(len(val)):
        val_to_count = val[i]
        counter = 0
        
        for j in range(i, len(val)):
            if val[j] == val_to_count:
                counter += 1
            else:
                i = j + 1
                break 
        
        val_dict[val_to_count] = counter
        i += 1

    for key, val in val_dict.items():
        ans_str += str(val) + str(key)
    
    return ans_str

print(next_look_and_say(1)) 
print(next_look_and_say(11))
print(next_look_and_say(21))
    