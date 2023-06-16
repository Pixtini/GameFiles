import random, time , pandas as pd, itertools, warnings, numpy as np, datetime, operator, copy
import GMF as gmf
import TestStats as stat

st = time.time()
warnings.filterwarnings('ignore')
config = "/Users/connorkelly/Documents/Work/GameFiles/Test Game/TestConfig.xlsx"

symbol_table = pd.read_excel(config, 'reels')
pay_symbols = list(symbol_table.iloc[:,0])

def build_reels(symbol_table):
    reels = gmf.anyways_reel_builder([4,4,4,4,4,4], 6, symbol_table)
    return reels

def payout_calc(wins): 
    payouts = pd.read_excel(config, 'paytable')
    gmf.payout_calc(wins, payouts)
    gmf.print_wins(wins)

def winline_win_evulation(reels, pay_symbols, mixed_wins, winline, paytable):
    mixed_total, wins  = [0 for i in range(len(reels))], [0 for i in range(list(paytable.iloc[:0,])[1])]
    winline_to_check = [reels[i][winline[j-1]] for i, j in enumerate(winline)]
    print(winline_to_check)
    print(list(paytable.iloc[:0,])[1:])
    
    if set(winline_to_check).isdisjoint(set(mixed_wins)):
        for i, win in enumerate(list(paytable.iloc[:0,])[1:]):
            print(f"{win} + { winline_to_check.count(winline_to_check[0])}")
            if winline_to_check.count(winline_to_check[0]) == win:
                print("Success")
                wins[win-1] += 1
    
    print(wins)
    '''
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
    '''

    return wins

def set_one():
    reels = build_reels(symbol_table)
    gmf.print_reels(reels)
    winlines = gmf.winlines(pd.read_excel(config, 'winlines'))
    paytable = pd.read_excel(config, 'paytable')
    winline_win_evulation(reels, pay_symbols, ["Wild", "L1"] , winlines[0], paytable)


set_one()