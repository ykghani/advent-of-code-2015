#AOC 2015 - Day 14
'''
--- Day 14: Reindeer Olympics ---

This year is the Reindeer Olympics! Reindeer can fly at high speeds, but must rest occasionally to recover their energy. Santa would like to know which of his reindeer is fastest, and so he has them race.

Reindeer can only either be flying (always at their top speed) or resting (not moving at all), and always spend whole seconds in either state.

For example, suppose you have the following Reindeer:

Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds. / Means comet moves 140 km in 137 sec 
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
After one second, Comet has gone 14 km, while Dancer has gone 16 km. After ten seconds, Comet has gone 140 km, while Dancer has gone 160 km. On the eleventh second, Comet begins resting (staying at 140 km), and Dancer continues on for a total distance of 176 km. On the 12th second, both reindeer are resting. They continue to rest until the 138th second, when Comet flies for another ten seconds. On the 174th second, Dancer flies for another 11 seconds.

In this example, after the 1000th second, both reindeer are resting, and Comet is in the lead at 1120 km (poor Dancer has only gotten 1056 km by that point). So, in this situation, Comet would win (if the race ended at 1000 seconds).

Given the descriptions of each reindeer (in your puzzle input), after exactly 2503 seconds, what distance has the winning reindeer traveled?
'''

import re

file_path = './d14/d14_input.txt'

RACE_TIME = 2503
pattern = re.compile(r'(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds\.')
part_one_flag = False

class Reindeer:
    
    points = 0
    pos = 0
    rest_flag = False
    rest_counter = 0
    flight_counter = 0
    
    def __init__(self, name, speed, flight_time, rest_time):
        self.name = name
        self.speed = int(speed)
        self.flight_time = int(flight_time)
        self.rest_time = int(rest_time)
    
    def __repr__(self):
        return f'Deer {self.name} with speed {self.speed}, flight time {self.flight_time}, and resting time {self.rest_time} has {self.points} points at pos: {self.pos}'
    
    def update_points(self):
        self.points += 1
    
    def update_position(self): 
        
        if self.rest_flag:
            self.rest_counter += 1
        else:
            self.pos += self.speed
            self.flight_counter += 1
        
        if self.flight_counter == self.flight_time:
            self.rest_flag = True
            self.flight_counter = 0
        elif self.rest_counter == self.rest_time:
            self.rest_flag = False
            self.rest_counter = 0
        
        return

def part_one(name, speed, flight_time, rest_time):
    dist = 0
    speed, flight_time, rest_time = int(speed), int(flight_time), int(rest_time)
    
    dist += RACE_TIME // (flight_time + rest_time) * (speed * flight_time)
    remainder = RACE_TIME % (flight_time + rest_time)
    if remainder > flight_time: 
        dist += flight_time * speed 
    else:
        dist += remainder * speed 
    
    return dist 

max_dist = 0 
stats = dict()
deers = []
with open(file_path, 'r') as file: 
    for line in file: 
        line = line.strip()
        match = pattern.match(line)
        
        if match: 
            name, speed, flight_time, rest_time = match.groups()
            speed, flight_time, rest_time = int(speed), int(flight_time), int(rest_time)
            
            deers.append(Reindeer(name, speed, flight_time, rest_time))
        
        if part_one_flag:
            dist = part_one(name, speed, flight_time, rest_time)
            if dist > max_dist:
                max_dist = dist 
file.close()

if part_one_flag:
    print(max_dist)
else:
    furthest_pos = 0
    for t in range(1, RACE_TIME + 1):
        furthest_deer = []

        for deer in deers: 
            deer.update_position()
            new_pos = deer.pos
            
            if new_pos > furthest_pos:
                furthest_pos = new_pos
                furthest_deer = [deer]
            elif new_pos == furthest_pos:
                furthest_deer.append(deer)
        
        for deer in furthest_deer:
            deer.update_points() 
        
max_points = max(deer.points for deer in deers)
print(max_points)
