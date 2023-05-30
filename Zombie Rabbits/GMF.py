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
            total_bonuses[i] += reels[j].count(bonus)
    return total_bonuses

def symbol_counter(reels,symbol):
    counts_per_reel = [0 for i in range(len(reels))]
    for y, reel in enumerate(reels):
        counts_per_reel[y] += reel.count(symbol)
    return counts_per_reel 

def anyways_win_evaluation(reels, mixed_wins):
    check_symbols, mixed_win_symbols = {}, {}
    for x, symbol in enumerate(mixed_wins):
        if symbol in mixed_win_symbols:
            continue
        mixed_win_symbols.update({symbol:symbol_counter(reels,symbol)})
        print(f"mixed are {mixed_win_symbols}")      

    for x, symbol in enumerate(reels[0]):
        if symbol in check_symbols or symbol in mixed_win_symbols:
            continue
        check_symbols.update({symbol:symbol_counter(reels,symbol)})
        print(f"chck are {check_symbols}")
        