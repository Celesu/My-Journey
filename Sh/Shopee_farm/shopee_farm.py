# Shopee Farm

def not_crossing(the_park, the_side):
    total_health = 0
    return total_health, the_side

def walking_through(the_park, the_side, M):
    possibilities = []
    sides = []
    if the_side == 'R':
        for i in range(1,M+1):
            total = sum(the_park[-i:])
            possibilities.append(total)
            if i == M:
                sides.append('R')
                possibilities.append(total)
                sides.append('L')
            else:
                sides.append('R')
    else:
        for i in range(M):
            total = sum(the_park[:i+1])
            possibilities.append(total)
            if i == M-1:
                sides.append('L')
                possibilities.append(total)
                sides.append('R')
            else:
                sides.append('L')
        
    return possibilities, sides

def max_health(the_park, current_day, N_days, M_cells, the_side = 'L', history = []):
    current_park=the_park[current_day-1]
    if current_day == N_days:
        hps, sides = walking_through(current_park, the_side, M_cells)
        positive_fruit = [x for x in hps if x > 0]
        if positive_fruit == []:
            hp, _ = not_crossing(current_park, the_side)
            history.append(hp)
            return hp
        else:
            history.append(max(positive_fruit))
            return max(positive_fruit)
    else:
        hps, sides = walking_through(current_park, the_side, M_cells)
        loc = [x for x, _ in enumerate(hps) if _ >= 0]
        positive_fruit = [hps[x] for x in loc]
        if positive_fruit == []:
            hp, side = not_crossing(current_park, the_side)
            return hp + max_health(the_park, current_day+1, N_days, M_cells, side) 
        else:
            for index_i, i in enumerate(sides):
                value = hps[index_i] + max_health(the_park, current_day+1, N_days, M_cells, i, [])
                history.append(value)
            return max(history)


T = int(input())
for i in range(T):
    N, M = [int(x) for x in input().split(" ")]
    A = []
    for ii in range(N):
        A.append([int(x) for x in input().split(" ")])
        
    print(max_health(A,1,N,M))


# Test case

# the_input = """3
# 1 5
# -9 -8 1 2 3
# 2 3
# 1 4 -5
# -1 -9 100
# 2 8
# 1 4 -5 7 2 8 -20 -1
# -1 -1 100 -30 -41 -444 732 -99"""

# a = [i for i in the_input.split("\n")]
# x = []
# for i in a:
#     x.append([int(ii) for ii in i.split(" ")])
    
# T = x.pop(0)[0]
# for i in range(T):
#     N, M = x.pop(0)
#     A = []
#     for i in range(N):
#         A.append(x.pop(0))    
    
#     print(max_health(A, 1, N, M))
