import random, time , pandas as pd, itertools, warnings, numpy as np, datetime, copy
test_reels = [['Coin', 'Coin', 'Coin', 'Coin'], [], ['Transform', 'Coin'], ['Coin', 'Coin', 'Coin', 'Coin'], ['Coin']]

def print_reels(reels):
    '''
    DEBUGGING TOOL

    Prints the reels in a clear manner
    '''
    for i, reel in enumerate(reels):
        print(str(reel))
    print("\n")

def print_wins(wins):
    '''
    DEBUGGING TOOL

    Prints the wins in a clear manner
    '''
    for i, win in enumerate(wins):
        print(f"{win} : {wins.get(win)}")
    print("\n")    

def selection(weights):
    '''
    SIM FUNCTION

    Generates an array of positions based on weights given to be able to select from i.e [3,0,2] will given 3 position 0, 0 position 1 and 2 position 2 to select from
    '''
    selectionpool = []
    for i, x in enumerate(weights): # Generates a pool of indicies based on weights to random.choice later
        for j in range(x):
            selectionpool.append(str(i))
    return selectionpool

def bonus_counter(reels, bonuses):
    '''
    SIM FUNCTION

    Returns an array of the quantiy of each of the bonuses given on the reels
    '''
    total_bonuses = [0 for i in range(len(bonuses))]
    for i, bonus in enumerate(bonuses):
        for j, reel in enumerate(reels):
            total_bonuses[i] += reels[j].count(bonus)
    return total_bonuses

def symbol_counter(reels,symbol):
    '''
    SIM FUNCTION

    Returns a count of how many of said symbol are on each reel
    '''
    counts_per_reel = [0 for i in range(len(reels))]
    for y, reel in enumerate(reels):
        counts_per_reel[y] += reel.count(symbol)
    return counts_per_reel 

def anyways_win_evaluation(reels, symbols, mixed_wins):
    '''
    GAME FUNCTION

    Checks the reels for any wins

    Input:
        reels: the reels that will be checked for the wins
        symbols: all regular symbols that will be checked agaisnt
        mixed_wins: all symbols that are involved in other wins
    
    Output:
        A dictionary that gives each symbol with an array of the length of how many reels there are with the number of occurances up til that reel
    '''
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
    
    removal = []
    for i in range(len(mixed_total)):
        if i == 0:
            removal.append(mixed_total[i])
        else:
            removal.append(removal[i-1]*mixed_total[i])

    for x, win in enumerate(wins):
        for y, occurances in enumerate(wins.get(win)):
            wins[win][y] -= removal[y]

    for x, win in enumerate(wins):
        for y, occurances in enumerate(wins.get(win)):
            if y+1 == len(wins.get(win)):
                continue
            if wins.get(win)[y+1] != 0:
                wins.get(win)[y] = 0
            else:
                continue

    return wins

def symbol_count(reels, symbol):
    '''
    GAME FUNCTION

    Checks the reels for any scatters and returns the count

    Input:
        reels: the reels that will be checked for the scatters
        scatters: all regular symbols that will be checked agaisnt
    
    Output:
        A dictionary that gives each symbol with an array of the length of how many reels there are with the number of occurances up til that reel
    '''
    count = 0 
    for x , reel in enumerate(reels):
        count += reel.count(symbol)
    return count

def anyways_reel_builder(height, length, st):
    '''
    GAME FUNCTION

    Spins the reels

    Input:
        height: an array of the desired heights of each reel
        length: how many reels there are
        st: symbol table pandas dataframe with the weights of each symbol per reel

    Output:
        2D Array of symbols that are randomly rolled base on the criterea 
    '''
    reels = []
    for i in range(1,length+1):
        st['prob'] = (st.iloc[:,i])/(st.iloc[:,i].sum())
        reels.append(list(np.random.choice(st['Symbols'],height[i-1] ,p = st['prob'], replace= True )))
    return reels

def position_finder(reels, to_find):
    '''
    SIM FUNCTION

    Returns a list of tuples of all positions of the given symbol within the reels
    '''
    positions = []
    for i, reel in enumerate(reels):
        for j, pos in enumerate(reel):
            if pos == to_find:
                positions.append((i,j))
    return positions 

def is_in(reels, symbol):
    '''
    SIM FUNCTION

    Returns boolean based on wether the symbol given is within the reels
    '''
    if symbol in list(itertools.chain(*reels)):
        return True
    else:
        return False

def reel_lengths(reels):
    '''
    SIM FUNCTION

    Returns the lengths of all reels into an list
    '''
    reel_leng = []
    for i, reel in enumerate(reels):
        reel_leng.append(len(reel))
    return reel_leng

def travelling_symbols(reels, symbol_table, travelling_symbol):
    '''
    GAME FEATURE

    Will move the stated travelling symbol down by one position and then perform a respin

    Inputs:
        reels - the reels which the function will be performed on
        symbol_table - possible symbols which the respin will happen (pandas dataframe)
        travelling_symbol - the symbol which will move can be any

    Output:
        respun reels which all travelling symbols have moved down by one position
    '''
    TW1_pos = position_finder(reels,travelling_symbol) 
    
    reels = anyways_reel_builder(reel_lengths(reels),6,symbol_table)
    
    for i, pos in enumerate(TW1_pos):
        if pos[1]+1 != len(reels[pos[0]]):
            reels[pos[0]][pos[1]+1] = travelling_symbol
    return reels

def replace(reels, x, y):
    '''
    GAME FEATURE

    Replace symbol x with symbol y

    Inputs:
        reels - the reels which the function will be performed on
        x - what will be replaced
        y - replaced with

    Output:
        Reels with symbol y inplaced of symbol x
    '''
    for i, reel in enumerate(reels):
        for j, symbol in enumerate(reel):
            if symbol == x:
                reels[i][j] = y
    return reels

def payout_calc(wins, payouts):
    '''
    SIM Feature

    Multiply Wins by Payouts

    Inputs:
        wins - number of wins
        payouts - payouts for each symbol

    Output:
        Return of the wins
    '''
    for x, win in enumerate(wins):
        for i in range(6):
            wins[win][i] = wins[win][i]*int(payouts.iloc[x][-i-1])
    return wins

def transform_reel(reels, transformed_into):
    '''
    Game Feature

    Transforms a reel into another symbol

    Inputs:
        reels - Game Reels
        transformed_into - What the symbols will be transformed into upon completion
    Output:
        Reels with one reel transformed
    '''
    transform_loc = position_finder(reels, "Transform")[0][0]
    weights = [1 for i in range(len(reels))]
    weights[transform_loc] = 0
    transform_reel = int(random.choice(selection(weights))) 

    for x, symbol in enumerate(reels[transform_reel]):
        reels[transform_reel][x] = transformed_into

    return reels
 

            

            

