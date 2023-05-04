import random
import pandas as pd
import numpy as np
import itertools
import warnings
import time
from datetime import date
st = time.time()
warnings.filterwarnings('ignore')

# Config, reads from config.xlsx file and puts it into array 
config = "/Users/connorkelly/Documents/Work/PythonWorkspace/BaseMirrorBonuses/config.xlsx"
n_mirror_table = pd.read_excel(config, 'data', usecols=[0,1])
bonus_table = pd.read_excel(config, 'data', nrows = 5, usecols=[3,4])
stored = bonus_table.bweights
bonus_table_inital = pd.read_excel(config, 'data', nrows = 5, usecols=[6,7])
results_file = open("DracsStacksResults"+str(date.today())+str(st)+".txt", "w")

# Globals
mirror_type = ["Coin","Multiplier","Scatter","Transform","Collect","SuperScatter"]
accumulated = [0,0,0,0,0,0] # Coins, Multiplier, Scatters, Transforms, Collect, SuperScatter

# bonus_choice will pick a bonus for the mirrors at random, given some constraints it will set the weights of certain features to zero to meet those constraints
def bonus_choice(scatter_count, mirror_count, collect_count, transform_count, new_selects, first_placement, reels):
    global bonus_table, bonus_table_inital, mirror_type, stored
    bonuses = []
    # Check if its the first placement, as there is additional weights for the intital placements and we need at least 1 Coin into the reels to begin with 
    if first_placement == True:
        bonuses.append("Coin")
        bonus_table.bweights = bonus_table_inital.cweights
    else:
        bonus_table.bweights = stored
    # The for loop below will be run once for all calls except the first placement 
    for i in range(new_selects):
        # Below sets the weights according to constraints
        if scatter_count == 3:
            bonus_table.bweights[2]=0 
        if mirror_count == 30 or transform_count == 1 or np.count_nonzero(np.asarray(list(itertools.chain(*reels)))) == 30:
            bonus_table.bweights[3]=0  
        if collect_count == 1:
            bonus_table.bweights[4]=0
        # Picks a Bonus at random according to the weights and appends to the bonuses array thats returned
        bonus_table['prob'] = (bonus_table.bweights)/(bonus_table.bweights.sum())
        selected = np.random.choice(bonus_table['bonus'],1 ,p = bonus_table['prob'], replace= False )[0] - 1
        bonuses.append(mirror_type[selected])
        # Adjusts counts of 
        if selected == 2:
            scatter_count += 1
        if selected == 3:
            transform_count += 1
        if selected == 4:
            collect_count += 1
    return bonuses

# Function picks a random reel based on if the reel is full or not
def reel_selector(reels, scatter):
    if scatter:
        weights = [0,1,1,1,0]
        for i, reel in enumerate(reels):
            if "Scatter" in reel:
                weights[i] = 0
    else:
        weights = [1,1,1,1,1]
    #Uniformly distrubuted across the reels
    for i, reel in enumerate(reels): #Sets the full reels weights to zero
        if len(reel) == 6:
            weights[i] = 0      
    selectionpool = []
    for i, x in enumerate(weights): # Generates a pool of indicies based on weights to random.choice later
        for j in range(x):
            selectionpool.append(str(i))
    return selectionpool

# bonus_counter counts the occurances of each of the bonus types on the reel and also sums the collected coins 
def bonus_counter(reels):
    global mirror_type
    counts = [0,0,0,0,0,0,0]
    for reel in reels: 
        for i, mirror in enumerate(mirror_type): # Checks each reels for each Bonus
            counts[i] += reel.count(mirror)
        for j, symbol in enumerate(reel): # Sums the collected coins 
            if symbol not in mirror_type:
                counts[6] += int(reel[j])
    return counts

# transform assesses the transform bonuses by adding additional mirrors to one reel and rerolling the transform
def transform(reels):
    global accumulated
    transform_loc = [(i,j)for i in [0,1,2,3,4] for j in reels[i] if j == "Transform"] # Find the locations of transform in the array
    transform_reel = int(random.choice(reel_selector(reels,False))) # Selects a non-full reel to transform at random
    for j in range(6 - int(len(reels[transform_reel]))): # Fills the reel with Bonuses
        counts = bonus_counter(reels)
        if (transform_reel == 1 or transform_reel == 2 or transform_reel == 3) and "Scatter" not in reels[transform_reel]:
            reels[transform_reel].append(bonus_choice(counts[2],sum(counts),counts[4],counts[3],1,False,reels)[0])
        else:
            reels[transform_reel].append(bonus_choice(3,sum(counts),counts[4],counts[3],1,False,reels)[0])
    accumulated[3] += 1 
    counts = bonus_counter(reels) # Re-roll the Transform Symbol
    if (transform_loc[0][0] == 1 or transform_loc[0][0] == 2 or transform_loc[0][0] == 3) and "Scatter" not in reels[transform_loc[0][0]]:
        reels[transform_loc[0][0]][reels[transform_loc[0][0]].index("Transform")] = bonus_choice(counts[2],sum(counts),counts[4],counts[3],1,False,reels)[0]
    else:
        reels[transform_loc[0][0]][reels[transform_loc[0][0]].index("Transform")] = bonus_choice(3,sum(counts),counts[4],counts[3],1,False,reels)[0]
    return reels

# multiplier assesses the multiplier bonueses by adding them to an accumlated pool and rereolling the multiplier
def multiplier(reels):
    global accumulated
    multiplier_loc = [(i,j)for i in [0,1,2,3,4] for j in reels[i] if j == "Multiplier"] # Find the locations of multipliers in the array
    for i, locations in enumerate(multiplier_loc): # Re-roll the Multiplier Symbols and increments the accumlated array
        accumulated[1] += 1
        counts = bonus_counter(reels)
        if (multiplier_loc[i][0] == 1 or multiplier_loc[i][0] == 2 or multiplier_loc[i][0] == 3) and "Scatter" not in reels[multiplier_loc[i][0]]:
            reels[multiplier_loc[i][0]][reels[multiplier_loc[i][0]].index("Multiplier")] = bonus_choice(counts[2],sum(counts),counts[4],counts[3],1,False,reels)[0]
        else:
            reels[multiplier_loc[i][0]][reels[multiplier_loc[i][0]].index("Multiplier")] = bonus_choice(3,sum(counts),counts[4],counts[3],1,False,reels)[0]
    return reels

# collect assesses the collects by adding all the coins visible and giving said collect that value and rerolling all coins
def collect(reels):
    global accumulated
    accumulated[4] += 1 
    coin_loc = [(i,j)for i in [0,1,2,3,4] for j in reels[i] if j == "Coin"] # Find the locations of Coins in the array
    collect_loc = [(i,j)for i in [0,1,2,3,4] for j in reels[i] if j == "Collect"] # Find the locations of Collects in the array
    reels[collect_loc[0][0]][reels[collect_loc[0][0]].index("Collect")] = len(coin_loc) # Sets Collect to the number of Coins on the reels
    for i, locations in enumerate(coin_loc): # Re-roll the Coin Symbols
        counts = bonus_counter(reels)
        if (coin_loc[i][0] == 1 or coin_loc[i][0] == 2 or coin_loc[i][0] == 3) and "Scatter" not in reels[coin_loc[i][0]]:
            reels[coin_loc[i][0]][reels[coin_loc[i][0]].index("Coin")] = bonus_choice(counts[2],sum(counts),counts[4],counts[3],1,False,reels)[0]
        else:
             reels[coin_loc[i][0]][reels[coin_loc[i][0]].index("Coin")] = bonus_choice(3,sum(counts),counts[4],counts[3],1,False,reels)[0]
    return reels

def super_scatter(reels):
    global accumulated
    scatter_table = pd.read_excel(config, 'data', nrows = 2, usecols=[15,16])
    scatter_table['prob'] = (scatter_table.fweights)/(scatter_table.fweights.sum())
    selected = np.random.choice(scatter_table['supers'],1 ,p = scatter_table['prob'], replace= False )[0]
    if selected == 1:
        reels[2][reels[2].index("Scatter")] = "SuperScatter"
        accumulated[5] += 1
        accumulated[2] -= 1
    return reels

# Prints the arrays into an easier to understand format
def print_reels(reels):
    for i, reel in enumerate(reels):
        print(str(reel))
    print("\n")
                    
def bonus_assessment():
    global n_mirror_table, inital_mirror_choice, final_mirror_count
    reels = [[],[],[],[],[]]
    #Intialize the starting Mirrors
    n_mirror_table['prob'] = (n_mirror_table.weights)/(n_mirror_table.weights.sum()) # Selects an starting Choice of Mirrors at random and intialises that many onto the reels
    inital_mirror_choice = np.random.choice(n_mirror_table['n_mirrors'], 1 ,p = n_mirror_table['prob'], replace = False)[0]
    mirrors = bonus_choice(0,inital_mirror_choice,0,0,inital_mirror_choice-1,True,reels)
    scatter_count = mirrors.count("Scatter")
    for i in range(scatter_count):
        reels[int(random.choice(reel_selector(reels,True)))].append("Scatter")
        mirrors.remove("Scatter")
    for mirror in mirrors: # Assigns the mirrors
        reels[int(random.choice(reel_selector(reels,False)))].append(mirror)
    #Sums Multipliers, preforms the Transforms then Collects until no more appear on reels
    while "Multiplier" in list(itertools.chain(*reels)) or "Transform" in list(itertools.chain(*reels)):
        reels = multiplier(reels)
        while "Transform" in list(itertools.chain(*reels)):
            reels = transform(reels)
        while "Collect" in list(itertools.chain(*reels)) and "Multiplier" not in list(itertools.chain(*reels)) and "Transform" not in list(itertools.chain(*reels)): #All Multipliers and Transforms must be assessed before Collects
            reels = collect(reels)
    if "Scatter" in reels[2]: #Randomly Rolls if Super Scatter will be placed instead of Regular Scatter
        super_scatter(reels)
    accumulated[0] = bonus_counter(reels)[0]+bonus_counter(reels)[6]
    accumulated[2] = bonus_counter(reels)[2]
    final_mirror_count = np.count_nonzero(np.asarray(list(itertools.chain(*reels))))

def coin_value_picker(): # Selects and returns a random coin value
    coin_table = pd.read_excel(config, 'data', nrows = 12, usecols=[9,10])
    coin_table['prob'] = (coin_table.dweights)/(coin_table.dweights.sum())
    selected = np.random.choice(coin_table['coin'],1 ,p = coin_table['prob'], replace= False )[0]
    return selected

def multiplier_value_picker(): # Selects and returns a random multiplier value
    multiplier_table = pd.read_excel(config, 'data', nrows = 4, usecols=[12,13])
    multiplier_table['prob'] = (multiplier_table.eweights)/(multiplier_table.eweights.sum())
    selected = np.random.choice(multiplier_table['multiplier'],1 ,p = multiplier_table['prob'], replace= False )[0]
    return selected

def main(sim_flag,coin_e,multiplier_e): 
    global accumulated
    bonus_assessment() # Perform a spin
    coin_value, multiplier_value = 0, 0
    if sim_flag:
        coin_value = accumulated[0]*coin_e
        multiplier_value = accumulated[1]*multiplier_e
    else:
        for i in range(accumulated[0]):
            coin_value += coin_value_picker()
        for i in range(accumulated[1]):
            multiplier_value += multiplier_value_picker()

    if multiplier_value == 0: # Calculates the final return (by total bet)
        total_bet_return = coin_value/10
    else:
        total_bet_return = (coin_value*multiplier_value)/10
    results_file.write(f"{total_bet_return}\t{accumulated[0]}\t{accumulated[1]}\t{accumulated[2]}\t{accumulated[3]}\t{accumulated[4]}\t{accumulated[5]}\t{inital_mirror_choice}\t{final_mirror_count}\n")
    result = [total_bet_return, accumulated[2]]
    return result

def simulation(trials):
    global accumulated
    coin_table = pd.read_excel(config, 'data', nrows = 12, usecols=[9,10]) # Figure out expected value of coins
    coin_table['prob'] = (coin_table.dweights)/(coin_table.dweights.sum())
    coin_table['expected'] = coin_table.coin*coin_table.prob
    coin_e = coin_table['expected'].sum()

    multiplier_table = pd.read_excel(config, 'data', nrows = 4, usecols=[12,13]) # Figure out expected value of mulitpliers
    multiplier_table['prob'] = (multiplier_table.eweights)/(multiplier_table.eweights.sum())
    multiplier_table['expected'] = multiplier_table.multiplier*multiplier_table.prob
    multiplier_e = multiplier_table['expected'].sum()

    results_file.write(f"Trials\t{trials}\nCoin Expected Value \t {coin_e} \nMultiplier Expected Value \t {multiplier_e} \n\n")
    results_file.write(f"Return\t{mirror_type[0]}\t{mirror_type[1]}\t{mirror_type[2]}\t{mirror_type[3]}\t{mirror_type[4]}\t{mirror_type[5]}\tStarting Mirrors\tEnd Mirrors\n")
    interval = 1000
    results = [0,0]
    for i in range(trials):
        result = main(True,coin_e,multiplier_e)
        results[0] += result[0]
        results[1] += result[1]
        accumulated = [0,0,0,0,0,0]
        if i%interval == 0:
            print(f"progress {time.time()-st} , {i//interval}/{trials//interval} ")
    print(f"For {trials} Trials - \n Average Pay: {results[0]/trials} \n Average Scatters: {results[1]/trials}")

simulation(100000)
et = time.time()
print(f"Execution time = {et-st} Seconds")





