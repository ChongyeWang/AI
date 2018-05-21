import random
import numpy as np
import math
import copy
import sys

__author__ = "Chongye Wang"


def normalize(w):
    for idx in range(0, len(w)):
        for i in range(0, len(w[idx])):
            w[idx][i] =  random.uniform(0, 0.1)


def affine_forward(X, W, b):
    #X : n * d
    #W : d * d_
    #b : d_

    Z = X.dot(W)
    for i in range(0, len(Z)):
        Z[i] = Z[i] + b

    return Z, (X, W, b)


def cross_entropy(F, y):
    n = len(F)

    loss = 0
    for i in range(0, n):
        action = int(y[i])

        sum = 0
        for k in range(0, 3):
            sum += math.e**F[i][k]
        sum = math.log(sum)
        loss += F[i][action] - sum
    loss = loss * (-1.0 / n)

    dF = np.zeros(F.shape)

    for i in range(0, n):
        total = 0.0
        for k in range(0, 3):
            total += math.e**F[i][k]
        #print(total)

        for j in range(0, len(F[i])):
            indicator = 0
            if j == y[i]: indicator = 1
            else: indicator = 0
            dF[i][j] = (indicator - math.e**F[i][j] / total) * (-1.0 / n)


    return loss, dF


def affine_backward(dZ, cache):

    A = cache[0]
    W = cache[1]
    b = cache[2]

    n = len(A)  #size of batch
    d = len(A[0]) #size of feature (5)
    d_ = len(W[0]) #size of neurons (256)


    dA = dZ.dot(W.T)
    dW = A.T.dot(dZ)
    db = np.array([sum(dZ[:, j]) for j in range(len(dZ[0]))])

    return dA, dW, db

def relu_forward(Z):
    A = np.zeros(Z.shape)
    for i in range(0, len(Z)):
        for j in range(0, len(Z[i])):
            if Z[i][j] > 0: A[i][j] = Z[i][j]
    return A, Z


def relu_backward(dA, cache):
    dZ = np.zeros(dA.shape)

    for i in range(0, len(cache)):
        for j in range(0, len(cache[0])):
            if cache[i][j] > 0.0: dZ[i][j] = dA[i][j]
            else: dZ[i][j] = 0.0
    return dZ


def three_network(X, w1, w2, w3, b1, b2, b3, y, test):
    Z1, acache1 = affine_forward(X, w1, b1)
    A1, rcache1 = relu_forward(Z1)

    #print(A1.shape) #150 * 256

    Z2, acache2 = affine_forward(A1, w2, b2)
    A2, rcache2 = relu_forward(Z2)
    F, acache3 = affine_forward(A2, w3, b3)


    if test == True:
        return

    loss, dF = cross_entropy(F, y)

    dA2, dW3, db3 = affine_backward(dF, acache3)

    dZ2 = relu_backward(dA2, rcache2)
    dA1, dW2, db2 = affine_backward(dZ2, acache2)

    dZ1 = relu_backward(dA1, rcache1)
    dX, dW1, db1 = affine_backward(dZ1, acache1)


    new_w1 = w1 - 0.1 * dW1
    new_w2 = w2 - 0.1 * dW2
    new_w3 = w3 - 0.1 * dW3

    new_b1 = b1 - 0.1 * db1
    new_b2 = b2 - 0.1 * db2
    new_b3 = b3 - 0.1 * db3

    for i in range(0, len(new_w1)):
        for j in range(0, len(new_w1[0])):
            w1[i][j] = new_w1[i][j]

    for i in range(0, len(new_w2)):
        for j in range(0, len(new_w2[0])):
            w2[i][j] = new_w2[i][j]

    for i in range(0, len(new_w3)):
        for j in range(0, len(new_w3[0])):
            w3[i][j] = new_w3[i][j]

    for i in range(0, len(new_b1)):
        b1[i] = new_b1[i]

    for i in range(0, len(new_b2)):
        b2[i] = new_b2[i]

    for i in range(0, len(new_b3)):
        b3[i] = new_b3[i]

    return loss


def neural_network(data, epoch, w1, w2, w3, b1, b2, b3, test):


    data_size = len(data)
    batch_size = 128
    for inx in range(0, epoch):
        random.shuffle(data)
        batch =[data[i:i + batch_size] for i in xrange(0, len(data), batch_size)]

        for i in range(0, data_size / batch_size):
            batch_data = batch[i]

            X = np.array([list[0:5] for list in batch_data])

            y = np.array([list[5] for list in batch_data])

            loss = three_network(X, w1, w2, w3, b1, b2, b3, y, test)

            print(loss)

def get_action(X, w1, w2, w3, b1, b2, b3):
    Z1, acache1 = affine_forward(X, w1, b1)
    A1, rcache1 = relu_forward(Z1)
    Z2, acache2 = affine_forward(A1, w2, b2)
    A2, rcache2 = relu_forward(Z2)
    F, acache3 = affine_forward(A2, w3, b3)

    curr_max = -sys.maxsize
    curr_action = -1
    for action in range(0, 3):
        if F[0][action] > curr_max:
            curr_max = F[0][action]
            curr_action = action

    return curr_action


if __name__ == "__main__":
    data = []
    with open("data.txt") as input:
        for line in input:
            data.append([float(i) for i in line.split()])

    w1 = np.zeros((5, 256))
    w2 = np.zeros((256, 256))
    w3 = np.zeros((256, 3))

    normalize(w1)
    normalize(w2)
    normalize(w3)


    b1 = np.zeros(256)
    b2 = np.zeros(256)
    b3 = np.zeros(3)

    test = False


    neural_network(data, 500, w1, w2, w3, b1, b2, b3, test)

    result = []

    for i in range(0, 200):

        paddle_height = 0.2

        ball_x = random.uniform(0, 1)
        ball_y = random.uniform(0, 1)

        velocity_x = 0.03
        velocity_y = 0.01

        paddle_y = 0.5 - paddle_height / 2

        X = np.array([[ball_x, ball_y, velocity_x, velocity_y, paddle_y]])

        num_rebound = 0
        while True:
            #1 : do not move
            #0 : move up
            #2 : move down
            action = get_action(X, w1, w2, w3, b1, b2, b3)

            if action == 1: paddle_y = paddle_y
            elif action == 0: paddle_y -= 0.04
            else: paddle_y += 0.04

            if paddle_y < 0: paddle_y = 0
            if paddle_y > 0.8: paddle_y = 0.8

            ball_x = ball_x + velocity_x
            ball_y = ball_y + velocity_y


            if ball_y < 0:
                ball_y = -ball_y
                velocity_y = -velocity_y
            if ball_y > 1:
                ball_y = 2.0 - ball_y
                velocity_y = -velocity_y
            if ball_x < 0:
                ball_x = -ball_x
                velocity_x = -velocity_x

            if ball_x > 1:
                if ball_y >= paddle_y and ball_y <= paddle_y + 0.2:
                    num_rebound += 1
                    ball_x = 2.0 - ball_x
                    velocity_x = -velocity_x + random.uniform(-0.015, 0.015)
                    if abs(velocity_x) < 0.03: velocity_x = -0.03
                    velocity_y = velocity_y + random.uniform(-0.03, 0.03)
                else:
                    break

            X = np.array([[ball_x, ball_y, velocity_x, velocity_y, paddle_y]])

        result.append(num_rebound)
        print(num_rebound)

    average = sum(result) / 200.0
    print(average)#13.325
