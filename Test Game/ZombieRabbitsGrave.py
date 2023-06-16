import random, time , pandas as pd, itertools, warnings, numpy as np, datetime, operator, copy
import GMF as gmf
import ZRStats as stat

st = time.time()
warnings.filterwarnings('ignore')
config = "/Users/connorkelly/Documents/Work/Games/Zombie Rabbits/Zombie Rabbits Config.xlsx"

symbol_table = pd.read_excel(config, 'reels')
pay_symbols = list(symbol_table.iloc[:,0])

def build_reels(symbol_table):
    reels = gmf.anyways_reel_builder([4,4,4,4,4,4], 6, symbol_table)
    return reels

def rabbit_num():
    return random.randint(0,7)

def full_moon(reels):
    full_moon_table = pd.read_excel(config, 'data', nrows = 2, usecols=[3,4])
    full_moon_table['prob'] = (full_moon_table.BWeights)/(full_moon_table.BWeights.sum())
    if np.random.choice(full_moon_table['FullMoon'],1 ,p = full_moon_table['prob'], replace= False )[0]:
        gmf.replace(reels, "TW1", "TW2")
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
    return

def TW1(reels, wins):
    while gmf.is_in(reels, 'TW1'):
        reels = gmf.travelling_symbols(reels, symbol_table, "TW1")
        new_wins = gmf.anyways_win_evaluation(reels, pay_symbols,["Wild", "TW1"])

        for x, win in enumerate(new_wins):
            if win not in wins:
                wins.update({win:new_wins.get(win)})
            else:
                wins[win] = list(map(operator.add, wins.get(win), new_wins.get(win)))
    return wins      

def TW2(reels, wins):
    multipliers = TW2_multipliers(reels,[0 for i in range(6)])
    new_wins = TW2_Involvment(reels, wins, TW2_multipliers(reels,multipliers))

    for x, win in enumerate(new_wins):
        if win not in wins:
            wins.update({win:new_wins.get(win)})
        else:
            wins[win] = list(map(operator.add, wins.get(win), new_wins.get(win)))

    print("First Pass")
    gmf.print_reels(reels)
    gmf.print_wins(new_wins)
    print(multipliers)

    while gmf.is_in(reels, 'TW2'):
        reels = gmf.travelling_symbols(reels, symbol_table, "TW2")
        new_wins = gmf.anyways_win_evaluation(reels, pay_symbols,["Wild", "TW1", "TW2"])

        multipliers = TW2_multipliers(reels,multipliers)
        new_wins = TW2_Involvment(reels, new_wins, TW2_multipliers(reels,multipliers))
        
        for x, win in enumerate(new_wins):
            if win not in wins:
                wins.update({win:new_wins.get(win)})
            else:
                wins[win] = list(map(operator.add, wins.get(win), new_wins.get(win)))
        
        print("Respin")
        gmf.print_reels(reels)
        gmf.print_wins(new_wins)
        print(multipliers)
    return wins

def TW2_multipliers(reels, multipliers):
    TW2_pos = gmf.position_finder(reels,"TW2")
    tw_table = pd.read_excel(config, 'tw2')
    tw_table['prob'] = (tw_table.Weights)/(tw_table.Weights.sum())
    for i, pos in enumerate(TW2_pos):
        multi = np.random.choice(tw_table['TW2 Multipliers'],1 ,p = tw_table['prob'], replace= True )[0]
        if multi > multipliers[pos[0]]:
            multipliers[pos[0]] = multi      
    return multipliers
    

def expand(reels, reel, i):
    symbol_table['prob'] = (symbol_table.iloc[:,i+1])/(symbol_table.iloc[:,i+1].sum())
    if reel[0] == 'Expand':
        reel[0] = np.random.choice(symbol_table['Symbols'],1 ,p = symbol_table['prob'], replace= True )[0]
        for j in range(random.randint(1,4)):
            reels[i].insert(1,np.random.choice(symbol_table['Symbols'],1 ,p = symbol_table['prob'], replace= True )[0])              
    return reel

def payout_calc(wins): 
    payouts = pd.read_excel(config, 'paytable')
    gmf.payout_calc(wins, payouts)
    gmf.print_wins(wins)

def popping(wins):
    to_be_popped = []
    for x, win in enumerate(wins):
        if wins.get(win)[2:6] == [0,0,0,0]:
            to_be_popped.append(win)
    for x, pop in enumerate(to_be_popped):
        wins.pop(pop)
    return wins

def TW2_Involvment(reels, wins, multipliers):
    tw2_passthrough = {}
    
    for x, win in enumerate(wins):
        temp = [copy.copy(reel) for i, reel in enumerate(reels)]
        for i, reel in enumerate(temp):
            for j, sym in enumerate(reel):
                if sym not in ["Wild", "TW1", 'TW2'] and sym != win:
                    temp[i][j] = "BLANK"
            for j in range(reel.count("BLANK")):
                reel.remove("BLANK")
        
        length = 0
        for y, occur in enumerate(wins.get(win)):
            if occur != 0:
                length = y + 1

        combos = [p for p in itertools.product(*(temp[i] for i in range(length)))]
        delete_combo = []
        for i, combo in enumerate(combos):
            if "TW2" not in combo:
                delete_combo.append(combo)
        for i, combo in enumerate(delete_combo):
            combos.remove(combo)
        
        tw2_passthrough.update({win:combos})

        additional_wins = []
        for z, combo in enumerate(tw2_passthrough.get(win)):
            additional_wins.append(0)
            for y, symbol in enumerate(combo):
                if symbol == "TW2":
                    additional_wins[z] += multipliers[y]
            additional_wins[z] -= 1

        for y, occur in enumerate(wins.get(win)):
            if occur != 0:
                wins[win][y] += sum(additional_wins)
    
    print(f"TW Passthrough")
    gmf.print_wins(tw2_passthrough)
    return wins

def TW_sim(total):
    reels = build_reels(symbol_table)
    rabbit_placement(reels)
    
    print("first placement")
    gmf.print_reels(reels)  
    
    print("TW1 to TW2")
    reels = full_moon(reels)
    gmf.print_reels(reels)

    wins = gmf.anyways_win_evaluation(reels, pay_symbols, ["Wild", "TW1", 'TW2'])
    gmf.print_wins(wins)
    
    if gmf.is_in(reels, "TW2"):
        TW2(reels, wins)
    
    print("WINS AWARDED")
    payout_calc(wins)


def set_one():
    reels = build_reels(symbol_table)
    gmf.print_reels(reels)
    wins = gmf.anyways_win_evaluation(reels, pay_symbols, ["Wild", "TW1", 'TW2'])
    scatters = gmf.symbol_count(reels,"SC1")
    payout_calc(wins)
    print(scatters)

set_one()