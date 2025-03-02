from constant import DICE, TOP, PRICE, CEIL, HELMET, WEAPON
from result_montecarlo import M_TOP, M_HELMET
from result_expectation import E_TOP, E_ARMOUR, E_WEAPON
from chowol import calc_chowol, gen_map



def calc_present():
    E_PARTS = E_ARMOUR
    GOLD_PUSH, GOLD_RESET = PRICE[1]
    LEVEL = 5
    COUNT_RESET = 5

    TURN_LIMIT = 4
    CHOWOL_MAP = "...b.w."

    ACTIVATE_REQ = (3 + 2 * (LEVEL >= 4) + 1 * (LEVEL >= 6))
    PITINESS = (COUNT_RESET >= ACTIVATE_REQ) * ((COUNT_RESET-ACTIVATE_REQ)//2 + 1)
    
    cur_prob, expected_push = calc_chowol(DICE[PITINESS],TURN_LIMIT,CHOWOL_MAP)
    cur_result = cur_prob*(expected_push*GOLD_PUSH)+(1-cur_prob)*(GOLD_RESET + E_PARTS[LEVEL-1][-(COUNT_RESET+2)] + GOLD_PUSH*TURN_LIMIT)
    print(f"현재 성공확률 : {cur_prob}")
    print(f"현재 기대비용 : {cur_result}, 복원 없이 성공시 누골 : {expected_push*GOLD_PUSH}")
    print(f"복원시 기대비용 : {GOLD_RESET + E_PARTS[LEVEL-1][-(COUNT_RESET+2)]}")
    
def calc_game():
    parts = int(input("초월 부위 (1:무기, 2:상의, 3:이외):"))
    E_PARTS = [E_WEAPON, E_TOP, E_ARMOUR][parts-1]
    GOLD_PUSH, GOLD_RESET = PRICE[parts!=1]
    
    LEVEL = int(input("초월 단계:"))
    ACTIVATE_REQ = (3 + 2 * (LEVEL >= 4) + 1 * (LEVEL >= 6))
    
    COUNT_RESET = int(input(f"복원 횟수(*참고: 엘조윈 1단계까지 {ACTIVATE_REQ}회 필요):"))
    PITINESS = (COUNT_RESET >= ACTIVATE_REQ) * ((COUNT_RESET-ACTIVATE_REQ)//2 + 1)
    print(f"현재 엘조윈의 가호 {PITINESS} 단계.")
    
    is_new = (input("새삥임? (Y/n):") != 'n')
    if is_new:
        NUM_TILE, NUM_SPECIAL_TILE, TURN_LIMIT = [WEAPON, TOP, HELMET][parts-1][LEVEL-1]
        num_w = 0

    CHOWOL_MAP = input("타일 입력 :")
    if is_new:
        while len(CHOWOL_MAP) != NUM_TILE:
            print(f"길이가 맞지 않음! (필요 길이:{NUM_TILE}, 입력된 길이:{len(CHOWOL_MAP)})")
            CHOWOL_MAP = input("타일 입력 :")
        while CHOWOL_MAP.count('.') != NUM_TILE-NUM_SPECIAL_TILE:
            print(f"특수타일 개수가 맞지 않음! (필요 개수:{NUM_SPECIAL_TILE}, 입력된 개수:{NUM_TILE-CHOWOL_MAP.count('.')})")
            CHOWOL_MAP = input("타일 입력 :")
    else:
        TURN_LIMIT = int(input("남은 턴 수:"))
        num_w = int(input("강화 석판(하얀) 밟은 횟수:"))
        
    while True:
        cur_prob, expected_push = calc_chowol(DICE[PITINESS],TURN_LIMIT,CHOWOL_MAP, num_w)
        cur_result = cur_prob*(expected_push*GOLD_PUSH)+(1-cur_prob)*(GOLD_RESET + E_PARTS[LEVEL-1][-(COUNT_RESET+2)] + GOLD_PUSH*TURN_LIMIT)
        print(f"현재 성공확률 : {cur_prob}")
        print(f"현재 기대비용 : {cur_result}, 복원 없이 성공시 누골 : {expected_push*GOLD_PUSH}")
        print(f"복원시 기대비용 : {GOLD_RESET + E_PARTS[LEVEL-1][-(COUNT_RESET+2)]}")
        
        dice = int(input("정화 결과(이동 칸 수):"))
        num_w += (input("강화 석판(하얀) 밟음? (y/N):")=='y')
        CHOWOL_MAP = CHOWOL_MAP[dice:]
        TURN_LIMIT -= 1