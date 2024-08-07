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
    out = ''
    
    if len(val) == 1:
        return str(val.count(val[0])) + val
    else:
        string_splits = []
        current = 1
        current_seq = val[0]
        for i in range(1, len(val)):
            if val[i] == current_seq[-1]:
                current_seq += val[i]
            else:
                string_splits.append(current_seq)
                current_seq = val[i]
        
        string_splits.append(current_seq)
        
        for seq in string_splits:
            count = seq.count(seq[0])
            out += str(count) + str(seq[0])
        
    return out 

val = INPUT
for _ in range(40):
    val = next_look_and_say(val)

print(f"Part 1 answer: {len(val)}")

for _ in range(10):
    val = next_look_and_say(val)

print(f"Part 2 answer is: {len(val)}")