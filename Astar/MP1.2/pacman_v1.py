
import sys
import time
import copy
import numpy as np
import collections

def findStart(maze):
    """
    Find the start position of the maze
    """
    start_Position = 0
    for i in range(0, len(maze)):
        for j in range(0, len(maze[0])):
            if maze[i][j] == 'P':
                start_Position = i * len(maze[0]) + j
                return start_Position
    return -1


def findEnd(maze):
    """
    Find the end position of the maze
    """
    final_Position = 0
    for i in range(0, len(maze)):
        for j in range(0, len(maze[0])):
            if maze[i][j] == '.':
                final_Position = i * len(maze[0]) + j
                return final_Position
    return -1


def distance(currX, currY, targetX, targetY):
    """
    Get the distance between two positions
    """
    return abs(currX - targetX) + abs(currY - targetY)



def Astar(maze, startX, startY, endX, endY):
    """
    Find the solution of the maze(A*)
    """
    #Get the width, height and size of maze
    width = len(maze[0])
    height = len(maze)
    size = width * height

    #Mark visited place
    visited = [0 for x in range(size)]

    #distance value
    f_value = [sys.maxsize for x in range(size)]
    #total value
    t_value = [sys.maxsize for x in range(size)]

    #Keep track of the position of parent node
    parent_Position = [0 for x in range(size)]

    #Keep track of the number of node expanded
    node_expanded = 0

    start_Position = startY * width + startX
    list = []
    list.append(start_Position)
    f_value[start_Position] = 0
    t_value[start_Position] = distance(startX, startY, endX, endY)

    while len(list) != 0:
        #find current best
        curr = findMin_Astar(list, t_value)
        currY = curr / width
        currX = curr % width
        if currX == endX and currY == endY:
            break
        #Target Position finded
        list.remove(curr)
        visited[curr] = 1

        #Increase the node expanded
        node_expanded += 1

        #Left
        if currX - 1 >= 0 and maze[currY][currX - 1] != '%':
            if visited[curr - 1] != 1:
                if curr - 1 not in list:
                    list.append(curr - 1)
                curr_val = f_value[curr] + 1
                if curr_val < f_value[curr - 1]:
                    f_value[curr - 1] = curr_val
                    t_value[curr - 1] = f_value[curr - 1] + distance((curr - 1) % width, (curr - 1) / width, endX, endY)
                    parent_Position[curr - 1] = curr

        #Right
        if currX + 1 < width and maze[currY][currX + 1] != '%':
            if visited[curr + 1] != 1:
                if curr + 1 not in list:
                    list.append(curr + 1)
                curr_val = f_value[curr] + 1
                if curr_val < f_value[curr + 1]:
                    f_value[curr + 1] = curr_val
                    t_value[curr + 1] = f_value[curr + 1] + distance((curr + 1) % width, (curr + 1) / width, endX, endY)
                    parent_Position[curr + 1] = curr

        #Up
        if currY - 1 >= 0 and maze[currY - 1][currX] != '%':
            if visited[curr - width] != 1:
                if curr - width not in list:
                    list.append(curr - width)
                curr_val = f_value[curr] + 1
                if curr_val < f_value[curr - width]:
                    f_value[curr - width] = curr_val
                    t_value[curr - width] = f_value[curr - width] + distance((curr - width) % width, (curr - width) / width, endX, endY)
                    parent_Position[curr - width] = curr

        #Down
        if currY + 1 < height and maze[currY + 1][currX] != '%':
            if visited[curr + width] != 1:
                if curr + width not in list:
                    list.append(curr + width)
                    curr_val = f_value[curr] + 1
                if curr_val < f_value[curr + width]:
                    f_value[curr + width] = curr_val
                    t_value[curr + width] = f_value[curr + width] + distance((curr + width) % width, (curr + width) / width, endX, endY)
                    parent_Position[curr + width] = curr

    step_cost = 0
    #Generate solution path
    position = endY * width + endX
    while position != start_Position:
        position = parent_Position[position]
        step_cost += 1

    return step_cost


def permutation(nums):
    """
    Get the permutation of the list
    """
    list = []
    temp = []
    backtrack(list, temp, nums)
    return list

def backtrack(list, temp, nums):
    """
    Helper function for permutation
    """
    if len(temp) == len(nums):
        list.append(temp[:])
    else:
        for i in range(0, len(nums)):
            if(nums[i] in temp):
                continue
            temp = temp + [nums[i]]
            backtrack(list, temp, nums)
            temp.pop()


def num_of_goals(maze):
    """
    Find the number of goals
    """
    count = 0
    for i in range(0, len(maze)):
        for j in range(0, len(maze[0])):
            if maze[i][j] == '.':
                count += 1
    return count


def list_of_points(maze):
    """
    Return positions of all points
    """
    result = []
    for i in range(0, len(maze)):
        for j in range(0, len(maze[0])):
            if maze[i][j] == '.':
                result.append((j, i))
    return result


def closest_fruit(maze, currX, currY, fruit_list):
    """
    This function finds the nearest fruit of current position
    """
    curr_min = sys.maxsize
    for position in fruit_list:
        distance = Astar(maze, currX, currY, position[0], position[1])
        if distance < curr_min:
            curr_min = distance
    return curr_min


def findMin_Astar(list, t_value):
    """
    Get the min f_value of a list
    """
    currMin = sys.maxsize
    result = 0
    for index in list:
        if t_value[index] < currMin:
            currMin = t_value[index]
            result = index
    return result


def findMin(list, t_value):
    """
    Get the min f_value of a list
    """
    currMin = sys.maxsize
    result = 0
    for index in list:
        if t_value[(index[0], index[1], tuple(index[2].items()))] < currMin:
            currMin = t_value[(index[0], index[1], tuple(index[2].items()))]
            result = index
    return result

def position_of_points(maze):
    """
    Get the position of points in a maze
    """
    result = {}
    count = 0
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == '.':
                result[(j, i)] = 1
    return result
###########################################

if __name__ == "__main__":

    #Initialize maze
    width = 0
    height = 0
    infile = open('tiny.txt', 'r')
    for line in infile:
        width = len(line)
        height = height + 1

    maze = [[0 for x in range(width)] for y in range(height)]
    infile = open('tiny.txt', 'r')
    w = 0
    h = 0
    for line in infile:
        w = 0
        for c in line:
            if w < width:
                maze[h][w] = c
            w += 1
        h += 1


    #Get the width, height and size of maze
    width = len(maze[0])
    height = len(maze)
    size = width * height

    #Position of start node
    start_Position = findStart(maze)
    startX = start_Position % width
    startY = start_Position / width

    #distance value
    f_value = {}
    #total value
    t_value = {}

    #Keep track of the number of node expanded
    node_expanded = 0

    #The number of fruits
    num_of_goals = num_of_goals(maze)

    #the order of founded fruits
    order_of_fruits = []

    #the position of all fruits
    orig_fruit_list = list_of_points(maze)

    #Get the position dict of points
    points_position = position_of_points(maze)

    #Goal state of maze
    goal_state = copy.deepcopy(points_position)
    goal_state = copy.deepcopy(goal_state)
    for key in goal_state:
        goal_state[key] = 0
    goal_state = tuple(goal_state.items())


    #visited :
    #0 : x coordinate of current player
    #1 : y coordinate of current player
    #2 : dict of points position
    visited = {}

    f_value[(startX, startY, tuple(points_position.items()))] = 0
    t_value[(startX, startY, tuple(points_position.items()))] = closest_fruit(maze, startX, startY, orig_fruit_list)

    #Keep track of total cost
    cost = 0

    #Keep track of node expanded
    node_expanded = 0

    list = []
    list.append((startX, startY, copy.deepcopy(copy.deepcopy(points_position))))

    parent = {}

    endX = 0
    endY = 0

    while len(list) != 0:
        print(list)
        print(t_value)
        #find current best
        curr = findMin(list, t_value)
        currX = curr[0]
        currY = curr[1]

        list.remove(curr)

        #Mark as visited
        visited[curr[0], curr[1], tuple(curr[2].items())] = 1

        find_all = False

        fruit_list1 = []
        for key in curr[2]:
            if curr[2][key] == 1:
                fruit_list1.append(key)

        #Check if any fruit is found
        for fruit in fruit_list1:
            if fruit[0] == currX and fruit[1] == currY:
                new_dict = copy.deepcopy(copy.deepcopy(curr[2]))
                new_dict[(currX, currY)] = 0
                new_fruit_list = []
                for key in new_dict:
                    if new_dict[key] == 1:
                        new_fruit_list.append(key)
                f_value[(currX, currY, tuple(new_dict.items()))] = f_value[(currX, currY, tuple(curr[2].items()))]
                t_value[(currX, currY, tuple(new_dict.items()))] = f_value[(currX, currY, tuple(new_dict.items()))] + closest_fruit(maze, currX, currY, new_fruit_list)

                parent[(currX, currY, tuple(new_dict.items()))] = parent[(currX, currY, tuple(curr[2].items()))]
                curr = (currX, currY, copy.deepcopy(copy.deepcopy(new_dict)))
                visited[(currX, currY, tuple(curr[2].items()))] = 1

                #Already find all the dots
                if tuple(new_dict.items()) == goal_state:
                    find_all = True
                    endX = currX
                    endY = currY
                    break

                #print(tuple(new_dict.items()))
                #print(goal_state)

                break

        if find_all == True:
            break


        node_expanded += 1

        #Left
        if currX - 1 >= 0 and maze[currY][currX - 1] != '%':
            orig = tuple(curr[2].items())
            orig_dict = copy.deepcopy(copy.deepcopy(curr[2]))
            if (currX - 1, currY, orig) not in visited:
                visited[(currX - 1, currY, orig)] = 0
            if visited[(currX - 1, currY, orig)] != 1:
                if (currX - 1, currY, orig_dict) not in list:
                    list.append((currX - 1, currY, orig_dict))
                #remainging list of fruits
                fruit_list = []
                for key in curr[2]:
                    if curr[2][key] == 1:
                        fruit_list.append(key)
                if (currX - 1, currY, orig) not in f_value:
                    f_value[(currX - 1, currY, orig)] = f_value[(currX, currY, orig)] + 1
                    t_value[(currX - 1, currY, orig)] = f_value[(currX - 1, currY, orig)] + closest_fruit(maze, currX - 1, currY, fruit_list)
                    parent[(currX - 1, currY, orig)] = (currX, currY, orig)
                else:
                    curr_val = f_value[(currX, currY, orig)] + 1
                    if curr_val < f_value[(currX - 1, currY, orig)]:
                        f_value[(currX - 1, currY, orig)] = curr_val
                        t_value[(currX - 1, currY, orig)] = f_value[(currX - 1, currY, orig)] + closest_fruit(maze, currX - 1, currY, fruit_list)
                        parent[(currX - 1, currY, orig)] = (currX, currY, orig)


        #Right
        if currX + 1 < width and maze[currY][currX + 1] != '%':
            orig = tuple(curr[2].items())
            orig_dict = copy.deepcopy(copy.deepcopy(curr[2]))
            if (currX + 1, currY, orig) not in visited:
                visited[(currX + 1, currY, orig)] = 0
            if visited[(currX + 1, currY, orig)] != 1:
                if (currX + 1, currY, orig_dict) not in list:
                    list.append((currX + 1, currY, orig_dict))
                #remainging list of fruits
                fruit_list = []
                for key in curr[2]:
                    if curr[2][key] == 1:
                        fruit_list.append(key)
                if (currX + 1, currY, orig) not in f_value:
                    f_value[(currX + 1, currY, orig)] = f_value[(currX, currY, orig)] + 1
                    t_value[(currX + 1, currY, orig)] = f_value[(currX + 1, currY, orig)] + closest_fruit(maze, currX + 1, currY, fruit_list)
                    parent[(currX + 1, currY, orig)] = (currX, currY, orig)
                else:
                    curr_val = f_value[(currX, currY, orig)] + 1
                    if curr_val < f_value[(currX + 1, currY, orig)]:
                        f_value[(currX + 1, currY, orig)] = curr_val
                        t_value[(currX + 1, currY, orig)] = f_value[(currX + 1, currY, orig)] + closest_fruit(maze, currX + 1, currY, fruit_list)
                        parent[(currX + 1, currY, orig)] = (currX, currY, orig)

        #Up
        if currY - 1 >= 0 and maze[currY - 1][currX] != '%':
            orig = tuple(curr[2].items())
            orig_dict = copy.deepcopy(copy.deepcopy(curr[2]))
            if (currX, currY - 1, orig) not in visited:
                visited[(currX, currY - 1, orig)] = 0
            if visited[(currX, currY - 1, orig)] != 1:
                if (currX, currY - 1, orig_dict) not in list:
                    list.append((currX, currY - 1, orig_dict))
                #remainging list of fruits
                fruit_list = []
                for key in curr[2]:
                    if curr[2][key] == 1:
                        fruit_list.append(key)
                if (currX, currY - 1, orig) not in f_value:
                    f_value[(currX, currY - 1, orig)] = f_value[(currX, currY, orig)] + 1
                    t_value[(currX, currY - 1, orig)] = f_value[(currX, currY - 1, orig)] + closest_fruit(maze, currX, currY - 1, fruit_list)
                    parent[(currX, currY - 1, orig)] = (currX, currY, orig)
                else:
                    curr_val = f_value[(currX, currY, orig)] + 1
                    if curr_val < f_value[(currX, currY - 1, orig)]:
                        f_value[(currX, currY - 1, orig)] = curr_val
                        t_value[(currX, currY - 1, orig)] = f_value[(currX, currY - 1, orig)] + closest_fruit(maze, currX, currY - 1, fruit_list)
                        parent[(currX, currY - 1, orig)] = (currX, currY, orig)

        #Down
        if currY + 1 < height and maze[currY + 1][currX] != '%':
            orig = tuple(curr[2].items())
            orig_dict = copy.deepcopy(copy.deepcopy(curr[2]))
            if (currX, currY + 1, orig) not in visited:
                visited[(currX, currY + 1, orig)] = 0
            if visited[(currX, currY + 1, orig)] != 1:
                if (currX, currY + 1, orig_dict) not in list:
                    list.append((currX, currY + 1, orig_dict))
                #remainging list of fruits
                fruit_list = []
                for key in curr[2]:
                    if curr[2][key] == 1:
                        fruit_list.append(key)
                if (currX, currY + 1, orig) not in f_value:
                    f_value[(currX, currY + 1, orig)] = f_value[(currX, currY, orig)] + 1
                    t_value[(currX, currY + 1, orig)] = f_value[(currX, currY + 1, orig)] + closest_fruit(maze, currX, currY + 1, fruit_list)
                    parent[(currX, currY + 1, orig)] = (currX, currY, orig)
                else:
                    curr_val = f_value[(currX, currY, orig)] + 1
                    if curr_val < f_value[(currX, currY + 1, orig)]:
                        f_value[(currX, currY + 1, orig)] = curr_val
                        t_value[(currX, currY + 1, orig)] = f_value[(currX, currY + 1, orig)] + closest_fruit(maze, currX, currY + 1, fruit_list)
                        parent[(currX, currY + 1, orig)] = (currX, currY, orig)

###########################################

    cost = f_value[(endX, endY, goal_state)]
    print(cost)

    print(node_expanded)

    start_state = (startX, startY, tuple(points_position.items()))
    curr_state = (endX, endY, goal_state)

    #reversed order of fruits visited
    order_of_fruits = []

    step_cost = 0
    while curr_state != start_state:
        prev_state = parent[curr_state]
        if prev_state[2] != curr_state[2]:
            for index in range(0, len(prev_state[2])):
                if prev_state[2][index][1] != curr_state[2][index][1]:
                    order_of_fruits.append(prev_state[2][index][0])
                    break
        curr_state = parent[curr_state]
        step_cost += 1

    print(step_cost)

    #Mark the order of dots
    symbol = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd' ,'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n']

    count = 0
    result_list = order_of_fruits[::-1]
    for fruit in result_list:
        maze[fruit[1]][fruit[0]] = symbol[count]
        count += 1
    print(result_list)

    result_maze = ""
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            result_maze = result_maze + maze[i][j]
        result_maze = result_maze + '\n'

    print(result_maze)


###########################################
