'''
AOC 2015 Day 17 - No Such Thing As Too Much 
'''

containers = sorted([50, 44, 11, 49, 42, 46, 18, 32, 26, 40, 21, 7, 18, 43, 10, 47, 36, 24, 22, 40])

def count_ways_to_stack_nog(amount, containers):
    dp = [0] * (amount + 1)
    dp[0] = 1
    
    for cont in containers: 
        for i in range(cont, amount + 1):
            dp[i] += dp[i - cont]
    
    return dp[amount]

print(f"Part 1 answer: {count_ways_to_stack_nog(150, containers)}")