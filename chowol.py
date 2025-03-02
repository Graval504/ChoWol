import sys
from random import choice, sample

def gen_map(NUM_TILE:int, NUM_SPECIAL_TILE:int, TURN_LIMIT:int):
    SPECAIL_TILES = ['r','y','b','m','w']
    chowol_map = ["."] * NUM_TILE
    for i in sample(range(1, NUM_TILE-1), NUM_SPECIAL_TILE):
        chowol_map[i] =  choice(SPECAIL_TILES)
    return ''.join(chowol_map)

def dfs(turn, idx, p1cnt, last, istriple, prob, s, N, dp, probv):
    idx = min(N - 1, idx)

    if s[idx] == 'b':
        dfs(turn, idx + last, p1cnt, last, istriple, prob, s, N, dp, probv)
    
    elif s[idx] == 'm':
        mov = 4 * (2 if istriple else 1)
        dfs(turn, idx + mov, p1cnt, mov, istriple, prob, s, N, dp, probv)
    
    elif s[idx] == 'y':
        for i in range(1, 5):
            mov = (i + p1cnt) * (2 if istriple else 1)
            dfs(turn, idx + mov, p1cnt, mov, istriple, prob * probv[i], s, N, dp, probv)
    
    elif s[idx] == 'r':
        if last != 0:
            dp[turn][idx][p1cnt] += prob
            return
        
        for i in range(1, 5):
            mov = (i + p1cnt) * 3
            dfs(turn, idx + mov, p1cnt, mov, True, prob * probv[i], s, N, dp, probv)
    
    elif s[idx] == 'w':
        if last != 0:
            dp[turn][idx][p1cnt + 1] += prob
            return
        
        for i in range(1, 5):
            mov = i + p1cnt
            dfs(turn, idx + mov, p1cnt, mov, False, prob * probv[i], s, N, dp, probv)
    
    else:
        if last != 0:
            dp[turn][idx][p1cnt] += prob
            return
        
        for i in range(1, 5):
            mov = i + p1cnt
            dfs(turn, idx + mov, p1cnt, mov, False, prob * probv[i], s, N, dp, probv)

def calc_chowol(dice:list[int], turn:int, chowol_map:str, num_w:int=0):
    sys.setrecursionlimit(10**6)
    
    probv = dice
    KMAX = 10
    
    s = chowol_map
    N = len(s)
    
    dp = [[[0.0 for _ in range(KMAX)] for _ in range(N)] for _ in range(turn+2)]
    dp[0][0][0+num_w] = 1.0
    
    for i in range(turn+1):
        for j in range(N - 1):
            for k in range(KMAX):
                if dp[i][j][k] == 0:
                    continue
                dfs(i + 1, j, k, 0, False, dp[i][j][k], s, N, dp, probv)
    
    result = []
    for i in range(turn+1):
        probsum = sum(dp[i][N - 1][k] for k in range(KMAX))
        # print(probsum)
        result.append(probsum)
    if sum(result) == 0:
        return 0, 0
    return sum(result), sum(i*v for i,v in enumerate(result))/sum(result)
