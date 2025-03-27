from constant import DICE, TOP, PRICE, HELMET
from chowol import calc_chowol, gen_map
from tqdm import tqdm


def calc_weapon(num_iter = 100000):
    for level in range(1,8):
        for pitiness in range(9):
            LEVEL = level
            PITINESS = pitiness

            prob_sum = 0
            expected_cost_sum = 0
            for i in range(num_iter):
                chowol_map = gen_map(*TOP[LEVEL-1])
                turn_limit = TOP[LEVEL-1][2] if PITINESS != 8 else 12
                result = calc_chowol(DICE[PITINESS], turn_limit, chowol_map)
                prob_sum += result[0]
                expected_cost_sum += result[0]*result[1]
            print(f"({prob_sum/num_iter}, {expected_cost_sum/prob_sum}),")
        print()

def calc_armour(num_iter = 100000):
    for level in range(1,8):
        for pitiness in range(9):
            LEVEL = level
            PITINESS = pitiness

            prob_sum = 0
            expected_cost_sum = 0
            for i in range(num_iter):
                chowol_map = gen_map(*HELMET[LEVEL-1])
                turn_limit = HELMET[LEVEL-1][2] if PITINESS != 8 else 12
                result = calc_chowol(DICE[PITINESS], turn_limit, chowol_map)
                prob_sum += result[0]
                expected_cost_sum += result[0]*result[1]
            print(f"({prob_sum/num_iter}, {expected_cost_sum/prob_sum}),")
        print()