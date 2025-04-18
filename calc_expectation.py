from constant import DICE, TOP, PRICE, HELMET, CEIL
from result_montecarlo import M_TOP, M_HELMET
from chowol import calc_chowol, gen_map
from tqdm import tqdm
import sys

def calc_weapon():
    result = 0
    cur_prob = 0
    for level in range(7,0,-1):
        print("[")
        pitiness_req = 4 + (level >= 4) + (level >= 6)
        for count_reset in range(CEIL[level-1],-1,-1):
            pitiness = (count_reset >= pitiness_req) * ((count_reset-pitiness_req)//2 + 1)
            result = (M_TOP[level-1][pitiness][0] * M_TOP[level-1][pitiness][1] * PRICE[0][0]) + (result+PRICE[0][1]) * (1-M_TOP[level-1][pitiness][0])
            cur_prob = M_TOP[level-1][pitiness][0] + cur_prob*(1-M_TOP[level-1][pitiness][0])
            print(f"{result},")
        print("],")

def calc_armour():
    result = 0
    cur_prob = 0
    for level in range(7,0,-1):
        print("[")
        pitiness_req = 4 + (level >= 4) + (level >= 6)
        for count_reset in range(CEIL[level-1],-1,-1):
            pitiness = (count_reset >= pitiness_req) * ((count_reset-pitiness_req)//2 + 1)
            result = (M_HELMET[level-1][pitiness][0] * M_HELMET[level-1][pitiness][1] * PRICE[1][0]) + (result+PRICE[1][1]) * (1-M_HELMET[level-1][pitiness][0])
            if pitiness != 8:
                result += PRICE[1][1]
            cur_prob = M_HELMET[level-1][pitiness][0] + cur_prob*(1-M_HELMET[level-1][pitiness][0])
            print(f"{result},")
        print("],")

def calc_top():
    result = 0
    cur_prob = 0
    for level in range(7,0,-1):
        print("[")
        pitiness_req = 4 + (level >= 4) + (level >= 6)
        for count_reset in range(CEIL[level-1],-1,-1):
            pitiness = (count_reset >= pitiness_req) * ((count_reset-pitiness_req)//2 + 1)
            result = (M_TOP[level-1][pitiness][0] * M_TOP[level-1][pitiness][1] * PRICE[1][0]) + (result+PRICE[1][1]) * (1-M_TOP[level-1][pitiness][0])
            if pitiness != 8:
                result += PRICE[1][1]
            cur_prob = M_TOP[level-1][pitiness][0] + cur_prob*(1-M_TOP[level-1][pitiness][0])
            print(f"{result},")
        print("],")
        
def write_expectation():
    origin_out = sys.stdout
    sys.stdout = open("result_expectation.py", "w")

    print("E_WEAPON = [")
    calc_weapon()
    print("][::-1]")

    print("E_TOP = [")
    calc_top()
    print("][::-1]")

    print("E_ARMOUR = [")
    calc_armour()
    print("][::-1]")

    sys.stdout.close()
    sys.stdout = origin_out
    return