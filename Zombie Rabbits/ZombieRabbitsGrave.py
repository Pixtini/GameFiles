import random, time , pandas as pd, itertools, warnings, numpy as np, datetime
import GMF as gmf
st = time.time()
warnings.filterwarnings('ignore')
config = "/Users/connorkelly/Documents/Work/Games/Zombie Rabbits/Zombie Rabbits Config.xlsx"

def grave_placement(reels):
    reels[random.randint(0,5)][random.randint(0,3)] = "Grave"
    return reels

def rabbit_num():
    return random.randint(0,7)

def full_moon(reels):
    full_moon_table = pd.read_excel(config, 'data', nrows = 2, usecols=[3,4])
    full_moon_table['prob'] = (full_moon_table.BWeights)/(full_moon_table.BWeights.sum())
    if np.random.choice(full_moon_table['FullMoon'],1 ,p = full_moon_table['prob'], replace= False )[0]:
        for i, reel in enumerate(reels):
            for j, symbol in enumerate(reel):
                if symbol == 'TW1':
                    reels[i][j] = "TW2"
    return reels       

def reel_selector(reels):
    weights = [1,1,1,1,1,1] #Uniformly distrubuted across the reels
    for i, reel in enumerate(reels): #Sets the full reels weights to zero
        if "Symbol" not in reel:
            weights[i] = 0      
    return gmf.selection(weights)

def sym_selector(reel,isTW):
    weights = [1 for i in range(len(reel))] #Uniformly distrubuted across the reel
    for i, symbol in enumerate(reel): #Sets the full reels weights to zero
        if symbol != "Symbol":
            weights[i] = 0
    if isTW:
        weights[len(weights)-1] = 0

    return gmf.selection(weights)

def rabbit_placement(reels):
    for i, reel in enumerate(reels):
        state = bin(rabbit_num())[2:]
        if len(state) == 1:
            state = "00"+state
        if len(state) == 2:
            state = "0" + state
        print(state)

        if state[0] == "1":
            reel[0] = "Expand"
            expand(reel,i)
        if state[1] == "1":
            reel[int(random.choice(sym_selector(reel,False)))] = "Wild"
        if state[2] == "1":
            reel[int(random.choice(sym_selector(reel,True)))] = "TW"
        gmf.print_reels(reels)
    return


def TW1():
    pass

def TW2():
    pass

def expand(reel,i):
    print(f"expanding on reel {i}")
    if reel[0] == 'Expand':
        reel[0] = "Symbol"
        for j in range(random.randint(1,4)): 
            reels[i].insert(1,"Symbol")              
    return reels

def counter(reels):
    global counts, total_count, total_bonuses
    total_count = 0
    for j, reel in enumerate(reels): # Checks each reels for each Bonus
        counts[j] += 4 - reel.count("Symbol") - reel.count("Grave")
        total_count += counts[j]
    total_bonuses = gmf.bonus_counter(reel, ["Wild", "Expand", "TW1", "TW2"])
    
def main():
    global counts, total_bonuses
    counts, total_bonuses = [0 for i in range(6)], [0 for i in range(4)]
    total = 10**1
    interval = total//10
    for i in range(total):
        reels = [["Symbol","Symbol","Symbol","Symbol"] for i in range(6)]
        rabbit_placement(reels)
        full_moon(reels)
        counter(reels)
        gmf.print_reels(reels)
        if i%interval == 0:
            print(f"{i//interval}/{total//interval} + {counts} + {total_bonuses}")
    print(f"{total_count} + {total} Graves")

reels = [["Symbol","Symbol","Symbol","Symbol"] for i in range(6)]
rabbit_placement(reels)
