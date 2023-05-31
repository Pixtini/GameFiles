import random, time , pandas as pd, itertools, warnings, numpy as np, datetime
import GMF as gmf
st = time.time()
warnings.filterwarnings('ignore')
config = "/Users/connorkelly/Documents/Work/Games/Zombie Rabbits/Zombie Rabbits Config.xlsx"

symbol_table = pd.read_excel(config, 'reels')
pay_symbols = list(symbol_table.iloc[:,0])

def build_reels(symbol_table):
    reels = gmf.anyways_reel_builder([4,4,4,4,4,4],6,symbol_table)
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

def sym_selector(reel,isTW,symbols):
    weights = [1 for i in range(len(reel))] #Uniformly distrubuted across the reel
    for i, symbol in enumerate(reel): #Sets the full reels weights to zero
        if symbol not in symbols:
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

        if state[0] == "1":
            reel[0] = "Expand"
            expand(reels,reel,i)
        if state[1] == "1":
            reel[int(random.choice(sym_selector(reel,False,pay_symbols)))] = "Wild"
        if state[2] == "1":
            reel[int(random.choice(sym_selector(reel,True,pay_symbols)))] = "TW1"
    #gmf.print_reels(reels)
    return

def TW1(reels):
    TW1_pos, reel_leng = [], []
    for i, reel in enumerate(reels):
        reel_leng.append(len(reel))
        for j, pos in enumerate(reel):
            if pos == 'TW1':
                TW1_pos.append((i,j))
    
    reels = gmf.anyways_reel_builder(reel_leng,6,symbol_table)
    
    for i, pos in enumerate(TW1_pos):
        if pos[1]+1 != len(reels[pos[0]]):
            reels[pos[0]][pos[1]+1] = "TW1"

    return reels

def TW_Count(reels):
    counts = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
    for i, reel in enumerate(reels):
        for j, symbol in enumerate(reel[::-1]):
            if symbol == "TW1":
                counts[i][j] += 1

    for k in range(len(counts)):
        counts[k] = counts[k][::-1]
    return counts

def highest_tw(reels):
    count = [0 for i in range(8)]
    highest = 0
    for i, reel in enumerate(reels):
        if 'TW1' in reel:
            if reel[::-1].index('TW1') > highest:
                highest = reel[::-1].index('TW1')
    count[highest] += 1
    return highest

def TW2():
    pass

def expand(reels,reel,i):
    symbol_table['prob'] = (symbol_table.iloc[:,i+1])/(symbol_table.iloc[:,i+1].sum())
    if reel[0] == 'Expand':
        reel[0] = np.random.choice(symbol_table['Symbols'],1 ,p = symbol_table['prob'], replace= True )[0]
        for j in range(random.randint(1,4)):
            reels[i].insert(1,np.random.choice(symbol_table['Symbols'],1 ,p = symbol_table['prob'], replace= True )[0])              
    return reel

def counter(reels):
    global counts, total_count, total_bonuses
    total_count = 0
    for j, reel in enumerate(reels): # Checks each reels for each Bonus
        counts[j] += 4 - reel.count("Symbol") - reel.count("Grave")
        total_count += counts[j]
    total_bonuses = gmf.bonus_counter(reel, ["Wild", "Expand", "TW1", "TW2"])


def TW_sim(total):
    total_counts = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
    total_pos = [0,0,0,0,0,0,0,0]

    interval = total//10

    for i in range(total):
        reels = build_reels(symbol_table)
        rabbit_placement(reels)
        temp = TW_Count(reels)
        gmf.print_reels(reels)
        for k, reel in enumerate(temp):
            for l, pos in enumerate(reel):
                total_counts[k][l] += temp[k][l]

        total_pos[highest_tw(reels)] += 1

        #if i%interval == 0:
            #print(f"{i//interval}/{total//interval}")
    gmf.print_reels(total_counts)
    print(total_pos)
    wins = gmf.anyways_win_evaluation(reels, pay_symbols,["Wild", "TW1"])
    gmf.print_wins(wins)
    TW1(reels)

TW_sim(1)