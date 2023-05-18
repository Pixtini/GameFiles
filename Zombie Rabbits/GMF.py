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