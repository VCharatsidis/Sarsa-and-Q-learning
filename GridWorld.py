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

def fill_transitions():
    for row in range(8):

        row_vals = []
        for col in range(8):
            col_vals = []

            for action in range(4):
                q_values.append(0)
                coords = []
                coords.append(row)
                coords.append(col)

                # North
                if action == 0:
                    if row - 1 > 0 and not check_walls(row-1, col):
                        coords[0] = row - 1

                # South
                elif action == 2:
                    if row+1 < 7 and not check_walls(row+1, col):
                        coords[0] = row + 1

                # West
                elif action == 3:
                    if col - 1 > 0 and not check_walls(row, col-1):
                        coords[1] = col-1

                # East
                elif action == 1:
                    if col + 1 < 7 and not check_walls(row, col+1):
                        coords[1] = col+1

                col_vals.append(coords)

            row_vals.append(col_vals)

        transitions.append(row_vals)


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
    next_state_x = transitions[x][y][action][0]
    next_state_y = transitions[x][y][action][1]
    next_action = random.randint(0, 3)
    q_values[x][y][action] = q_values[x][y][action] + alpha * (attribute_reword(next_state_x, next_state_y) + gamma * (q_values[next_state_x][next_state_y][next_action]- q_values[x][y][action]))
    return next_state_x, next_state_y, next_action

def simulator(runs):
    for i in range(runs):
        action = random.randint(0, 3)
        x,y = start()
