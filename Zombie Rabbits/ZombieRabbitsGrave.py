import random, time , pandas as pd, itertools, warnings, numpy as np, datetime
import GMF as gmf
st = time.time()
warnings.filterwarnings('ignore')

def grave_placement(reels):
    reels[random.randint(0,5)][random.randint(0,3)] = "Grave"
    return reels

def rabbit_num():
    return random.randint(2,24)

def full_moon():
    config = "/Users/connorkelly/Documents/Work/Games/Zombie Rabbits/Zombie Rabbits Config.xlsx"
    full_moon_table = pd.read_excel(config, 'data', nrows = 2, usecols=[3,4])
    full_moon_table['prob'] = (full_moon_table.BWeights)/(full_moon_table.BWeights.sum())
    return np.random.choice(full_moon_table['FullMoon'],1 ,p = full_moon_table['prob'], replace= False )[0] 

def reel_selector(reels):
    weights = [1,1,1,1,1,1] #Uniformly distrubuted across the reels
    for i, reel in enumerate(reels): #Sets the full reels weights to zero
        if "Symbol" not in reel:
            weights[i] = 0      
    return gmf.selection(weights)

def sym_selector(reel):
    weights = [1,1,1,1] #Uniformly distrubuted across the reel
    for i, symbol in enumerate(reel): #Sets the full reels weights to zero
        if symbol != "Symbol":
            weights[i] = 0      
    return gmf.selection(weights)

def rabbit_placement(reels):
    config = "/Users/connorkelly/Documents/Work/Games/Zombie Rabbits/Zombie Rabbits Config.xlsx"
    bonus_table = pd.read_excel(config, 'data', usecols=[0,1])
    bonus_table['prob'] = (bonus_table.Weights)/(bonus_table.Weights.sum())
    rabbits = np.random.choice(bonus_table['Bonus'],rabbit_num() ,p = bonus_table['prob'], replace= True )
    for i, rabbit in enumerate(rabbits):
        if i == 0:
            grave_placement(reels)
        else:
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
    global counts, total_count
    total_count = 0
    for j, reel in enumerate(reels): # Checks each reels for each Bonus
        counts[j] += 4 - reel.count("Symbol") - reel.count("Grave")
        total_count += counts[j]

def main():
    global counts
    counts = [0 for i in range(6)]
    total = 10**0
    interval = total
    for i in range(total):
        reels = [["Symbol","Symbol","Symbol","Symbol"] for i in range(6)]
        rabbit_placement(reels)
        bonus_counter(reels)
        gmf.print_reels(reels)
        if i%interval == 0:
            print(f"{i//interval}/{total//interval} + {counts}")
    print(f"{total_count} + {total} Graves")

main()
