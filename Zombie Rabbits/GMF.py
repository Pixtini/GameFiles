import random, time , pandas as pd, itertools, warnings, numpy as np, datetime 

def print_reels(reels):
    for i, reel in enumerate(reels):
        print(str(reel))
    print("\n")

def print_wins(wins):
    for i, win in enumerate(wins):
        print(f"{win} : {wins.get(win)}")
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

def anyways_win_evaluation(reels, symbols, mixed_wins):
    check_symbols, mixed_total, wins  = {}, [0 for i in range(len(reels))], {}
    
    for x, symbol in enumerate(mixed_wins):
        for i in range(len(reels)):
            mixed_total[i] += symbol_counter(reels,symbol)[i]

    for x, symbol in enumerate(symbols):
        if symbol in check_symbols or symbol in mixed_wins:
            continue
        
        check_symbols.update({symbol:symbol_counter(reels,symbol)})
        
        for i in range(len(reels)):
            check_symbols[symbol][i] += mixed_total[i]

    for x, symbol in enumerate(check_symbols):
        wins.update({symbol:[0 for i in range(len(reels))]})
        for y, count in enumerate(check_symbols.get(symbol)):
            if y == 0:
                wins[symbol][y] = count
            else:
                wins[symbol][y] = wins[symbol][y-1]*count
    
    return wins

def anyways_reel_builder(height, length, st):
    reels = []
    for i in range(1,length+1):
        st['prob'] = (st.iloc[:,i])/(st.iloc[:,i].sum())
        reels.append(list(np.random.choice(st['Symbols'],height[i-1] ,p = st['prob'], replace= True )))
    return reels



            

            

