#AOC 2015 - Day 16
'''
--- Day 16: Aunt Sue ---

Your Aunt Sue has given you a wonderful gift, and you'd like to send her a thank you card. However, there's a small problem: she signed it "From, Aunt Sue".

You have 500 Aunts named "Sue".

So, to avoid sending the card to the wrong person, you need to figure out which Aunt Sue (which you conveniently number 1 to 500, for sanity) gave you the gift. You open the present and, as luck would have it, good ol' Aunt Sue got you a My First Crime Scene Analysis Machine! Just what you wanted. Or needed, as the case may be.

The My First Crime Scene Analysis Machine (MFCSAM for short) can detect a few specific compounds in a given sample, as well as how many distinct kinds of those compounds there are. According to the instructions, these are what the MFCSAM can detect:

children, by human DNA age analysis.
cats. It doesn't differentiate individual breeds.
Several seemingly random breeds of dog: samoyeds, pomeranians, akitas, and vizslas.
goldfish. No other kinds of fish.
trees, all in one group.
cars, presumably by exhaust or gasoline or something.
perfumes, which is handy, since many of your Aunts Sue wear a few kinds.
In fact, many of your Aunts Sue have many of these. You put the wrapping from the gift into the MFCSAM. It beeps inquisitively at you a few times and then prints out a message on ticker tape:

children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1
You make a list of the things you can remember about each Aunt Sue. Things missing from your list aren't zero - you simply don't remember the value.

What is the number of the Sue that got you the gift?
'''
import re

file_path = './d16/d16_input.txt'

MFCSAM_OUTPUT = {'children': 3,
                 'cats': 7,
                 'samoyeds': 2,
                 'pomeranians': 3,
                 'akitas': 0,
                 'vizslas': 0,
                 'goldfish': 5,
                 'trees': 3,
                 'cars': 2,
                 'perfumes': 1}

sues = {}
suspects = []
with open(file_path, 'r') as file: 
    for line in file: 
        line = line.strip()
        line = line.split()
        suspects.append(line[1][: -1])
        sues[line[1][: -1]] = {line[2][: -1]: int(line[3][: -1]), line[4][: -1]: int(line[5][: -1]), 
                               line[6][: -1]: int(line[7])}
file.close()


while len(suspects) > 1: 
    for sue in suspects: 
        data = sues[sue]
        for attr in data: 
            if data[attr] != MFCSAM_OUTPUT[attr]:
                print(f"Can't be Sue #{sue}")
                suspects.remove(sue)
                break

print(suspects)    

#Part 2 
suspects = [str(_) for _ in range(1, 501)]
while len(suspects) > 1: 
    for sue in suspects:
        data = sues[sue]
        for attr in data: 
            if attr in ['cats', 'trees']:
                if data[attr] <= MFCSAM_OUTPUT[attr]:
                    suspects.remove(sue)
                    break
            elif attr in ['pomeranians', 'goldfish']:
                if data[attr] >= MFCSAM_OUTPUT[attr]:
                    suspects.remove(sue)
                    break
            else:
                if data[attr] != MFCSAM_OUTPUT[attr]:
                    suspects.remove(sue)
                    break

print(f'Part two answer is: {suspects}')