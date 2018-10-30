import random

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
                if check_walls(row, col):
                    q_values[row][col].append(-1)
                elif row == 7 and col == 7:
                    q_values[row][col].append(10)
                elif row == 5 and col == 4:
                    q_values[row][col].append(-20)
                else:
                    q_values[row][col].append(0)

                transitions[row][col][action][0] = row
                transitions[row][col][action][1] = col

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
    elif x == 7 and y == 7:
        return 10
    else:
        return -1


def start():
    x = random.randint(0, 7)
    y = random.randint(0, 7)

    while check_walls(x, y) or (x == 7 and y == 7) or (x == 5 and y == 4):
        x = random.randint(0, 7)
        y = random.randint(0, 7)

    return x, y


def q_learning(x, y):
    alpha = 0.3
    gamma = 0.9

    action = random.randint(0, 3)
    next_state_x = transitions[x][y][action][0]
    next_state_y = transitions[x][y][action][1]
    next_action = q_values[next_state_x][next_state_y].index(max(q_values[next_state_x][next_state_y]))

    qv = q_values[x][y][action]
    nqv = q_values[next_state_x][next_state_y][next_action]
    r = attribute_reword(next_state_x, next_state_y)

    q_values[x][y][action] = qv + alpha * (r + gamma * (nqv - qv))

    return next_state_x, next_state_y


def sarsa(x, y, action):
    alpha = 0.9
    gamma = 0.9
    # print("x "+str(x)+" y "+str(y)+" action "+str(action))
    # print("transitions[x][y][action][0] "+str(transitions[x][y][action][0]))
    # print("transitions[x][y][action][1] " + str(transitions[x][y][action][1]))
    # if random.uniform(0, 1) < 0.9:
    #     action = q_values[x][y].index(max(q_values[x][y]))
    # else:
    #     action = random.randint(0, 3)

    next_state_x = transitions[x][y][action][0]
    next_state_y = transitions[x][y][action][1]

    if random.uniform(0, 1) < 0.9:
        next_action = q_values[next_state_x][next_state_y].index(max(q_values[next_state_x][next_state_y]))
    else:
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
    x, y = start()
    episodes = 0
    action = random.randint(0,3)
    for i in range(runs):
        x, y, action = sarsa(x, y, action)
        #x, y, action = q_learning(x, y)

        if (x == 7 and y == 7) or (x == 5 and y == 4):
            action = random.randint(0,3)
            x, y = start()
            episodes += 1

        if x == 7 and y == 7:
            print("Error: program should terminate when reach T")
            break

        if x == 5 and y == 4:
            print("Error: program should terminate when reach S")
            break

        if check_walls(x, y):
            print("Error: program should not walk through wals")
            break

    print("episodes "+str(episodes))
    print_q()
    print_qvalues()


def print_q():
    global q_values

    for i in range(8):
        for j in range(8):

            if i == 7 and j == 7:
                print("T", end=" ")
            elif i == 5 and j == 4:
                print("S", end=" ")
            elif check_walls(i, j):
                print("W", end=" ")
            else:
                max_value_index = q_values[i][j].index(max(q_values[i][j]))
                print(str(max_value_index), end=" ")

        print("")


def print_qvalues():
    global q_values

    for i in range(8):
        for j in range(8):
            max_value = max(q_values[i][j])
            print(str(max_value), end=" ")

        print("")


simulator(10000000)