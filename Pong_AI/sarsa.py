"""This class implements the q_learning of pong"""
import random
import sys
import numpy as np
import time
import matplotlib.pyplot as plt


__author__ = "Chongye Wang"

def discrete_ball(ball_x, ball_y):
    discrete_ball_x = int(12 * ball_x)
    discrete_ball_y = int(12 * ball_y)
    if discrete_ball_x >= 12:
        discrete_ball_x = 11
    if discrete_ball_y >= 12:
        discrete_ball_y = 11
    return discrete_ball_x, discrete_ball_y

def discrete_velocity(velocity_x, velocity_y):
    discrete_velocity_x = 0
    discrete_velocity_y = 0
    if velocity_x > 0:
        discrete_velocity_x = 1
    else:
        discrete_velocity_x = -1
    if velocity_y >= 0.015:
        discrete_velocity_y = 1
    elif velocity_y <= -0.015:
        discrete_velocity_y = -1
    else:
        discrete_velocity_y = 0
    return discrete_velocity_x, discrete_velocity_y

def discrete_paddle(paddle_y):
    paddle_height = 0.2
    discrete_paddle_y = 0
    if paddle_y == 0.8:
        discrete_paddle_y = 11
    else:
        discrete_paddle_y = int((12 * paddle_y) / (1 - paddle_height))
    return discrete_paddle_y


def sarsa(Q, N, R):


    Ne = 5

    paddle_height = 0.2

    ball_x = 0.5
    ball_y = 0.5

    velocity_x = 0.03
    velocity_y = 0.01

    paddle_y = 0.5 - paddle_height / 2
    if paddle_y < 0:
        paddle_y = 0
    if paddle_y > 0.8:
        paddle_y = 0.8


    R['fail'] = -1

    Q['fail', 0] = -1
    Q['fail', -0.04] = -1
    Q['fail', 0.04] = -1



    discrete_ball_x, discrete_ball_y = discrete_ball(ball_x, ball_y)

    discrete_velocity_x, discrete_velocity_y = discrete_velocity(velocity_x, velocity_y)

    discrete_paddle_y = discrete_paddle(paddle_y)

    current_state = (discrete_ball_x, discrete_ball_y, discrete_velocity_x, discrete_velocity_y, discrete_paddle_y)


    R[current_state] = 0

    selected_action = selected_action = random.choice([0, 0.04, -0.04])


    while(current_state != 'fail'):

        #Update paddle position after selecting action
        paddle_y = paddle_y + selected_action
        if paddle_y < 0:
            paddle_y = 0
        if paddle_y > 0.8:
            paddle_y = 0.8


        current_state_action = (current_state, selected_action)

        curr_discrete_ball_x, curr_discrete_ball_y = discrete_ball(ball_x, ball_y)

        curr_discrete_velocity_x, curr_discrete_velocity_y = discrete_velocity(velocity_x, velocity_y)

        up_discrete_paddle_y = discrete_paddle(paddle_y)
        down_discrete_paddle_y = up_discrete_paddle_y + 2


        if current_state_action not in Q:
            Q[current_state_action] = 0

        if current_state_action not in N:
            N[current_state_action] = 1
        else:
            N[current_state_action] += 1



        ##########   next state   #########

        next_state = 0

        ball_x = ball_x + velocity_x
        ball_y = ball_y + velocity_y

        if ball_y < 0:
            ball_y = -ball_y
            velocity_y = -velocity_y
        if ball_y > 1:
            ball_y = 2 - ball_y
            velocity_y = -velocity_y
        if ball_x < 0:
            ball_x = -ball_x
            velocity_x = -velocity_x

        if ball_x > 1:

            if ball_y >= paddle_y and ball_y <= paddle_y + 0.2:

                ball_x = 2 * 1 - ball_x
                velocity_x = -velocity_x + random.uniform(-0.015, 0.015)
                if abs(velocity_x) < 0.03: velocity_x = -0.03
                velocity_y = velocity_y + random.uniform(-0.03, 0.03)

                curr_discrete_ball_x, curr_discrete_ball_y = discrete_ball(ball_x, ball_y)
                curr_discrete_velocity_x, curr_discrete_velocity_y = discrete_velocity(velocity_x, velocity_y)
                curr_discrete_paddle_y = discrete_paddle(paddle_y)

                next_state = (curr_discrete_ball_x, curr_discrete_ball_y, curr_discrete_velocity_x, curr_discrete_velocity_y, curr_discrete_paddle_y)

            else:
                next_state = 'fail'

        else:
            curr_discrete_ball_x, curr_discrete_ball_y = discrete_ball(ball_x, ball_y)
            curr_discrete_velocity_x, curr_discrete_velocity_y = discrete_velocity(velocity_x, velocity_y)
            curr_discrete_paddle_y = discrete_paddle(paddle_y)

            next_state = (curr_discrete_ball_x, curr_discrete_ball_y, curr_discrete_velocity_x, curr_discrete_velocity_y, curr_discrete_paddle_y)


        if curr_discrete_ball_x == 11 and (up_discrete_paddle_y <= curr_discrete_ball_y <= down_discrete_paddle_y):
            if current_state not in R:
                R[current_state] = 1
        elif curr_discrete_ball_x == 11 and (curr_discrete_ball_y < up_discrete_paddle_y or curr_discrete_ball_y > down_discrete_paddle_y):
            if current_state not in R:
                R[current_state] = -1
        else:
            if current_state not in R:
                R[current_state] = 0


        curr_max = -sys.maxsize
        selected_action = -1

        for action in [0, 0.04, -0.04]:
            state_action = (next_state, action)

            if state_action not in N:
                N[state_action] = 1
            else:
                N[state_action] += 1

            if state_action in N and N[state_action] > Ne:
                continue

            if state_action not in Q:
                Q[state_action] = 0
            if Q[state_action] > curr_max:
                selected_action = action
                curr_max = Q[state_action]


        if selected_action == -1:
            selected_action = random.choice([0, 0.04, -0.04])


        next_state_action = (next_state, selected_action)

        if next_state_action not in Q:
            Q[next_state_action] = 0


        learning_rate = 10.0 / (10.0 + N[current_state_action])

        Q[current_state_action] = Q[current_state_action] + learning_rate * (R[current_state] + 0.9 * Q[next_state_action] - Q[current_state_action])

        current_state = next_state



def test(Q):
    paddle_height = 0.2

    ball_x = 0.5
    ball_y = 0.5

    paddle_y = 0.5 - paddle_height / 2

    velocity_x = 0.03
    velocity_y = 0.01

    discrete_ball_x, discrete_ball_y = discrete_ball(ball_x, ball_y)
    discrete_velocity_x, discrete_velocity_y = discrete_velocity(velocity_x, velocity_y)
    discrete_paddle_y = discrete_paddle(paddle_y)

    current_state = (discrete_ball_x, discrete_ball_y, discrete_velocity_x, discrete_velocity_y, discrete_paddle_y)

    list = []
    count = 0

    position = []


    while(True):
        list.append((current_state[0], current_state[1], paddle_y))

        selected_action = -1
        curr_max = -sys.maxsize
        for action in [0, 0.04, -0.04]:
            state_action = (current_state, action)
            if state_action in Q and Q[state_action] > curr_max:
                selected_action = action
                curr_max = Q[state_action]

        if selected_action == -1:
            selected_action = random.choice([0, 0.04, -0.04])

        paddle_y = paddle_y + selected_action
        if paddle_y < 0:
            paddle_y = 0
        if paddle_y > 0.8:
            paddle_y = 0.8


        ball_x = ball_x + velocity_x
        ball_y = ball_y + velocity_y

        if ball_y < 0:
            ball_y = -ball_y
            velocity_y = -velocity_y
        if ball_y > 1:
            ball_y = 2 - ball_y
            velocity_y = -velocity_y
        if ball_x < 0:
            ball_x = -ball_x
            velocity_x = -velocity_x


        if ball_x > 1:
            if ball_y >= paddle_y and ball_y <= paddle_y + 0.2:

                ball_x = 2 * 1 - ball_x
                velocity_x = -velocity_x + random.uniform(-0.015, 0.015)
                if abs(velocity_x) < 0.03: velocity_x = -0.03
                velocity_y = velocity_y + random.uniform(-0.03, 0.03)
            else:
                break

        curr_discrete_ball_x, curr_discrete_ball_y = discrete_ball(ball_x, ball_y)

        curr_discrete_velocity_x, curr_discrete_velocity_y = discrete_velocity(velocity_x, velocity_y)

        up_discrete_paddle_y = discrete_paddle(paddle_y)
        down_discrete_paddle_y = up_discrete_paddle_y + 2


        curr_pos = (discrete_ball_x, discrete_ball_y)

        if curr_discrete_ball_x == 11 and up_discrete_paddle_y <= curr_discrete_ball_y <= down_discrete_paddle_y:
            if curr_pos != position[len(position) - 1]:
                count += 1

        position.append(curr_pos)


        discrete_ball_x, discrete_ball_y = discrete_ball(ball_x, ball_y)
        discrete_velocity_x, discrete_velocity_y = discrete_velocity(velocity_x, velocity_y)
        discrete_paddle_y = discrete_paddle(paddle_y)

        current_state = (discrete_ball_x, discrete_ball_y, discrete_velocity_x, discrete_velocity_y, discrete_paddle_y)

    return count, list

if __name__ == "__main__":

    Q = {}
    N = {}
    R = {}

    episode = []
    average_reward = []


    for num in range(0, 100000):
        sarsa(Q, N, R)
    
        if num >= 1000 and num % 500 == 0:
            total = 0
            for times in range(0, 200):
                count, list = test(Q)
                total += count
            average = total / 200.0
            episode.append(num)
            average_reward.append(average)

    plt.title("Sarsa - Mean Episode Reward")
    plt.xlabel("Episode")
    plt.ylabel("Reward")
    plt.plot(episode, average_reward, 'bo-')
    plt.show()

    exit()


    for i in range(0, 200):
        count, list = test(Q)
        print(count)




    animation = []
    for tuple in list:
        ball_x = tuple[0]
        ball_y = tuple[1]
        paddle_y = tuple[2]
        up_paddle_y = discrete_paddle(paddle_y)
        down_paddle_y = up_paddle_y + 2

        pong = np.chararray((12, 12))
        pong[:] = '.'
        pong[ball_y][ball_x] = 'B'
        for i in range(12):
            if i >= up_paddle_y and i <= down_paddle_y:
                pong[i][11] = 'I'

        animation.append(pong)

    for index in range(0, len(animation)):
        sys.stdout.write(str(animation[index]) + "\r")
        sys.stdout.flush()
        time.sleep(0.2)
