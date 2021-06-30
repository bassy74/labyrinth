import random
import numpy as np
import copy
import math

t = 0.3
alpha = 0.1
ganma = 0.9


def check(s):
    if s[0] <= 0 or s[0] > 6:
        return False
    elif s[1] <= 0 or s[1] > 6:
        return False
    elif s[1] == 2 and (s[0] == 2 or s[0] == 3 or s[0] == 4 or s[0] == 5):
        return False
    elif s[0] == 3 and (s[1] == 4 or s[1] == 5):
        return False
    elif s[1] == 5 and (s[0] == 5 or s[0] == 6):
        return False
    else:
        return True


def walk(goal, Q, turn):
    while turn > 0:
        s = [0] * 2
        while(1):
            # s[0] = random.randint(1, 6)
            # s[1] = random.randint(1, 6)
            if check(s) == True:
                break

        while(s != goal[0] and s != goal[1]):
            s_pre = copy.copy(s)
            Q_sum = 0
            p_direction = [0]*4
            for i in range(4):
                p_direction[i] = math.exp(Q[s_pre[0]+6*s_pre[1]-7][i]/t)
                Q_sum += p_direction[i]

            for i in range(4):
                p_direction[i] = p_direction[i] / Q_sum

            a = int(np.random.choice([0, 1, 2, 3], p=p_direction))
            if a == 0:
                s[0] += 1
            elif a == 1:
                s[1] -= 1
            elif a == 2:
                s[0] -= 1
            elif a == 3:
                s[1] += 1

            if check(s) == False:
                Q[s_pre[0]+6*s_pre[1]-7][a] = (1 - alpha) * \
                    Q[s_pre[0]+6*s_pre[1]-7][a] + alpha * (-0.1)
                s = copy.copy(s_pre)

            elif check(s) == True and s == goal[0]:
                Q[s_pre[0]+6*s_pre[1]-7][a] = (1 - alpha) * Q[s_pre[0]+6*s_pre[1]-7][a] + alpha * (
                    2 + ganma * max(Q[s[0]+6*s[1]-7]))

            elif check(s) == True and s == goal[1]:
                Q[s_pre[0]+6*s_pre[1]-7][a] = (1 - alpha) * Q[s_pre[0]+6*s_pre[1]-7][a] + alpha * (
                    1 + ganma * max(Q[s[0]+6*s[1]-7]))
            else:
                Q[s_pre[0]+6*s_pre[1]-7][a] = (1 - alpha) * Q[s_pre[0] +
                                                              6*s_pre[1]-7][a] + alpha * ganma * max(Q[s[0]+6*s[1]-7])

        turn -= 1
    return Q


q = [[1 for i in range(4)] for j in range(36)]
g = [[5, 4], [2, 5]]
print(walk(g, q, 100))
