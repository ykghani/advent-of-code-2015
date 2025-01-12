'''Advent of Code 2015 Day 25: Le tits now'''

ROW = 2981
COL = 3075

def calc_position(row: int, col: int) -> int:  
    '''Determines position in the diagonal fill sequence based on the row and col value'''
    diag = row + col - 1 
    d = 1
    for i in range(2, diag):
        d += i
    return d + col

pos = calc_position(ROW, COL)
val = 20151125
for _ in range(pos - 1):
    val = (val * 252533) % 33554393

print(f"Part one: {val}")