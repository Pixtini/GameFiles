import random, time , pandas as pd, itertools, warnings, numpy as np, datetime 

def print_reels(reels):
    for i, reel in enumerate(reels):
        print(str(reel))
    print("\n")

def selection(weights):
    selectionpool = []
    for i, x in enumerate(weights): # Generates a pool of indicies based on weights to random.choice later
        for j in range(x):
            selectionpool.append(str(i))
    return selectionpool

def bonus_counter(reels, bonuses):
    total_bonuses = [0 for i in range(len(bonuses))]
    for i, bonus in enumerate(bonuses):
        for j, reel in enumerate(reels):
            total_bonuses[i] += reel.count(bonus)
    return total_bonuses