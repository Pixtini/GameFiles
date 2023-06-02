import random, time , pandas as pd, itertools, warnings, numpy as np, datetime, operator, copy
import GMF as gmf
warnings.filterwarnings('ignore')

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

def tw_tracking(reels,temp):
    total_counts = [[0,0,0,0,0,0,0,0] for i in range(6)]
    total_pos = [0,0,0,0,0,0,0,0]    
    for k, reel in enumerate(temp):
        for l, pos in enumerate(reel):
            total_counts[k][l] += temp[k][l]
    total_pos[highest_tw(reels)] += 1