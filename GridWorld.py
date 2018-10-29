import random

world = []

fixed_rewords = [[]]


def fill_rewords():
    for row in range(8):
        row_vals = []

        for col  in range(8):
            row_vals.append(-1)

        fixed_rewords.append(row_vals)

    fixed_rewords[7][7] = 10
    fixed_rewords[5][4] = -20


transitions = [[[[]]]]
q_values = [[[]]]


def init():
    global transitions
    for row in range(8):
        transitions.append([])
        for col in range(8):
            transitions[row].append([])
            for action in range(4):
                transitions[row][col].append([])
                for coord in range(2):
                    transitions[row][col][action].append(0)


def fill_transitions():
    global q_values
    global transitions
    for row in range(8):
        q_values.append([])

        for col in range(8):
            # if check_walls(row, col):
            #     continue
            # if attribute_reword(row, col) != -1:
            #     continue

            q_values[row].append([])

            for action in range(4):
                q_values[row][col].append(0)

                print("row "+str(row)+" col "+str(col) + " action "+str(action))
                # North
                if action == 0:
                    if ((row - 1) >= 0) and (not check_walls(row-1, col)):
                        transitions[row][col][action][0] = row - 1

                # South
                elif action == 2:
                    if ((row + 1) <= 7) and (not check_walls(row+1, col)):
                        transitions[row][col][action][0] = row + 1

                # West
                elif action == 3:
                    if ((col - 1) >= 0) and (not check_walls(row, col-1)):
                        transitions[row][col][action][1] = col-1

                # East
                elif action == 1:
                    if ((col + 1) <= 7) and (not check_walls(row, col+1)):
                        transitions[row][col][action][1] = col+1

                print("row " + str(transitions[row][col][action][0]) + " col " + str(transitions[row][col][action][1]))


def check_walls(x, y):
    if x == 1 and 2 <= y <= 5:
        return True

    if y == 5 and 1 <= x <= 4:
        return True

    if x == 6 and 1 <= y <= 3:
        return True

    return False


def attribute_reword(x, y):
    if x == 5 and y == 4:
        return -20
    if x == 7 and y == 7:
        return 10

    return -1


def start():
    x = random.randint(0, 7)
    y = random.randint(0, 7)

    reword = attribute_reword(x, y)
    while check_walls(x, y) or reword != -1:
        x = random.randint(0, 7)
        y = random.randint(0, 7)

    return x, y


def sarsa(x, y, action):
    alpha = 0.9
    gamma = 0.9
    print("x "+str(x)+" y "+str(y)+" action "+str(action))
    print("transitions[x][y][action][0] "+str(transitions[x][y][action][0]))
    print("transitions[x][y][action][1] " + str(transitions[x][y][action][1]))
    next_state_x = transitions[x][y][action][0]
    next_state_y = transitions[x][y][action][1]
    next_action = random.randint(0, 3)

    qv = q_values[x][y][action]
    nqv = q_values[next_state_x][next_state_y][next_action]
    r = attribute_reword(next_state_x, next_state_y)

    q_values[x][y][action] = qv + alpha * (r + gamma * (nqv - qv))

    return next_state_x, next_state_y, next_action


def simulator(runs):
    global transitions
    global q_values
    init()
    fill_transitions()
    action = random.randint(0, 3)
    x, y = start()
    for i in range(runs):
        x, y, action = sarsa(x, y, action)

        if attribute_reword(x, y) != -1:
            action = random.randint(0, 3)
            x, y = start()

    print_q()


def print_q():
    for i in range(8):
        for j in range(8):
            print(str(q_values.index(max(q_values[i][j]))), end=" ")
        print("")


simulator(100000)