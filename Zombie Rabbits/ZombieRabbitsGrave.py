import random
import pandas as pd
import numpy as np
import itertools
import warnings
import time
from datetime import date
st = time.time()
warnings.filterwarnings('ignore')

def print_reels(reels):
    for i, reel in enumerate(reels):
        print(str(reel))
    print("\n")

def grave_placement(reels):
    reels[random.randint(0,5)][random.randint(0,3)] = "Grave"
    return reels

def rabbit_num():
    global rabbit_total
    x  = random.randint(1,23)
    rabbit_total += x
    return x

def reel_selector(reels):
    weights = [1,1,1,1,1,1] #Uniformly distrubuted across the reels
    for i, reel in enumerate(reels): #Sets the full reels weights to zero
        if "Symbol" not in reel:
            weights[i] = 0      
    selectionpool = []
    for i, x in enumerate(weights): # Generates a pool of indicies based on weights to random.choice later
        for j in range(x):
            selectionpool.append(str(i))
    return selectionpool

def sym_selector(reel):
    weights = [1,1,1,1] #Uniformly distrubuted across the reel
    for i, symbol in enumerate(reel): #Sets the full reels weights to zero
        if symbol != "Symbol":
            weights[i] = 0      
    selectionpool = []
    for i, x in enumerate(weights): # Generates a pool of indicies based on weights to random.choice later
        for j in range(x):
            selectionpool.append(str(i))
    return selectionpool

def rabbit_placement(reels):
    config = "/Users/connorkelly/Documents/Work/Games/Zombie Rabbits/Zombie Rabbits Config.xlsx"
    bonus_table = pd.read_excel(config, 'data', usecols=[0,1])
    bonus_table['prob'] = (bonus_table.Weights)/(bonus_table.Weights.sum())
    rabbits = np.random.choice(bonus_table['Bonus'],rabbit_num() ,p = bonus_table['prob'], replace= True )
    for i, rabbit in enumerate(rabbits):
        reel = int(random.choice(reel_selector(reels)))
        pos = int(random.choice(sym_selector(reels[reel])))
        reels[reel][pos] = rabbit


def TW1():
    pass

def TW2():
    pass

def expand(reels):
    for i, reel in enumerate(reels):
        for j, symbol in enumerate(reel):
            if symbol == 'Expand':
                reels[i][j] = "Symbol"
                reels[i].insert(j+1,"Symbol")              
    return reels

def bonus_counter(reels):
        global counts
        total_count = 0
        for j, reel in enumerate(reels): # Checks each reels for each Bonus
            counts[j] += 4 - reel.count("Symbol") - reel.count("Grave")
            total_count += counts[j]

def main(reels):
    global counts
    counts = [0 for i in range(6)]
    total = 10**5
    interval = total//100
    for i in range(total):
        reels = [["Symbol","Symbol","Symbol","Symbol"] for i in range(6)]
        grave_placement(reels)
        rabbit_placement(reels)
        bonus_counter(reels)
        if i%interval == 0:
            print(f"{i//interval}/{total//interval} + {counts}")
    print(rabbit_total)
    
    
rabbit_total = 0
reels = [["Symbol","Symbol","Symbol","Symbol"] for i in range(6)]
main(reels)
