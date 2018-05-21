import sys
import time
import numpy as np

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
        curr = findMin(list, t_value)
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

def findMin(list, t_value):
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

###########################################

if __name__ == "__main__":
    #Initialize maze
    width = 0
    height = 0
    infile = open('big.txt', 'r')
    for line in infile:
        width = len(line)
        height = height + 1

    maze = [[0 for x in range(width)] for y in range(height)]
    infile = open('big.txt', 'r')
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
    #The number of remaining fruits
    remain = num_of_goals

    #the order of founded fruits
    order_of_fruits = []

    #the position of all fruits
    fruit_list = list_of_points(maze)

    list = []
    list.append((startX, startY, remain))

    #visited :
    #0 : x coordinate of current player
    #1 : y coordinate of current player
    #2 : number of remaining goals
    visited = {}

    f_value[(startX, startY, remain)] = 0
    t_value[(startX, startY, remain)] = closest_fruit(maze, startX, startY, fruit_list)

    #Keep track of total cost
    cost = 0

    #Keep track of node expanded
    node_expanded = 0

    while len(list) != 0:

        #find current best
        curr = findMin(list, t_value)
        currX = curr[0]
        currY = curr[1]

        #Check if all the fruits have been found
        find_all = False

        #Check if any fruit is found
        for fruit in fruit_list:
            if fruit[0] == currX and fruit[1] == currY:
                remain -= 1
                order_of_fruits.append((currX, currY))
                fruit_list.remove((currX, currY))

                #Update f_value and t_value
                f_value[(currX, currY, remain)] = f_value[(currX, currY, remain + 1)]
                t_value[(currX, currY, remain)] = f_value[(currX, currY, remain)] + closest_fruit(maze, currX, currY, fruit_list)

                #Update list
                list = []
                list.append((currX, currY, remain))

                #update visited
                visited = {}

                #Already find all the dots
                if remain == 0:
                    find_all = True
                    break

                break

        if find_all == True:
            cost = f_value[(currX, currY, remain)]
            break

        list.remove((currX, currY, remain))

        #Mark as visited
        visited[(currX, currY, remain)] = 1

        node_expanded += 1

        #Left
        if currX - 1 >= 0 and maze[currY][currX - 1] != '%':
            if (currX - 1, currY, remain) not in visited:
                visited[(currX - 1, currY, remain)] = 0
            if visited[(currX - 1, currY, remain)] != 1:
                if (currX - 1, currY, remain) not in list:
                    list.append((currX - 1, currY, remain))
                if (currX - 1, currY, remain) not in f_value:
                    f_value[(currX - 1, currY, remain)] = f_value[(currX, currY, remain)] + 1
                    t_value[(currX - 1, currY, remain)] = f_value[(currX - 1, currY, remain)] + closest_fruit(maze, currX - 1, currY, fruit_list)
                else:
                    curr_val = f_value[(currX, currY, remain)] + 1
                    if curr_val < f_value[(currX - 1, currY, remain)]:
                        f_value[(currX - 1, currY, remain)] = curr_val
                        t_value[(currX - 1, currY, remain)] = f_value[(currX - 1, currY, remain)] + closest_fruit(maze, currX - 1, currY, fruit_list)


        #Right
        if currX + 1 < width and maze[currY][currX + 1] != '%':
            if (currX + 1, currY, remain) not in visited:
                visited[(currX + 1, currY, remain)] = 0
            if visited[(currX + 1, currY, remain)] != 1:
                if (currX + 1, currY, remain) not in list:
                    list.append((currX + 1, currY, remain))
                if (currX + 1, currY, remain) not in f_value:
                    f_value[(currX + 1, currY, remain)] = f_value[(currX, currY, remain)] + 1
                    t_value[(currX + 1, currY, remain)] = f_value[(currX + 1, currY, remain)] + closest_fruit(maze, currX + 1, currY, fruit_list)
                else:
                    curr_val = f_value[(currX, currY, remain)] + 1
                    if curr_val < f_value[(currX + 1, currY, remain)]:
                        f_value[(currX + 1, currY, remain)] = curr_val
                        t_value[(currX + 1, currY, remain)] = f_value[(currX + 1, currY, remain)] + closest_fruit(maze, currX + 1, currY, fruit_list)


        #Up
        if currY - 1 >= 0 and maze[currY - 1][currX] != '%':
            if (currX, currY - 1, remain) not in visited:
                visited[(currX, currY - 1, remain)] = 0
            if visited[(currX, currY - 1, remain)] != 1:
                if (currX, currY - 1, remain) not in list:
                    list.append((currX, currY - 1, remain))
                if (currX, currY - 1, remain) not in f_value:
                    f_value[(currX, currY - 1, remain)] = f_value[(currX, currY, remain)] + 1
                    t_value[(currX, currY - 1, remain)] = f_value[(currX, currY - 1, remain)] + closest_fruit(maze, currX, currY - 1, fruit_list)
                else:
                    curr_val = f_value[(currX, currY, remain)] + 1
                    if curr_val < f_value[(currX, currY - 1, remain)]:
                        f_value[(currX, currY - 1, remain)] = curr_val
                        t_value[(currX, currY - 1, remain)] = f_value[(currX, currY - 1, remain)] + closest_fruit(maze, currX, currY - 1, fruit_list)


        #Down
        if currY + 1 < height and maze[currY + 1][currX] != '%':
            if (currX, currY + 1, remain) not in visited:
                visited[(currX, currY + 1, remain)] = 0
            if visited[(currX, currY + 1, remain)] != 1:
                if (currX, currY + 1, remain) not in list:
                    list.append((currX, currY + 1, remain))
                if (currX, currY + 1, remain) not in f_value:
                    f_value[(currX, currY + 1, remain)] = f_value[(currX, currY, remain)] + 1
                    t_value[(currX, currY + 1, remain)] = f_value[(currX, currY + 1, remain)] + closest_fruit(maze, currX, currY + 1, fruit_list)
                else:
                    curr_val = f_value[(currX, currY, remain)] + 1
                    if curr_val < f_value[(currX, currY + 1, remain)]:
                        f_value[(currX, currY + 1, remain)] = curr_val
                        t_value[(currX, currY + 1, remain)] = f_value[(currX, currY + 1, remain)] + closest_fruit(maze, currX, currY + 1, fruit_list)


###########################################

    print(order_of_fruits)
    print(cost)
    print(node_expanded)

    print(f_value[(currX, currY, 0)])

    #Mark the order of dots
    #symbol = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd' ,'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n']

    animation = []
    prevX = startX
    prevY = startY
    animation.append(maze)
    for index in range(0, len(order_of_fruits)):
        maze[prevY][prevX] = ' '
        curr = order_of_fruits[index]
        maze[curr[1]][curr[0]] = 'P'
        prevX = curr[0]
        prevY = curr[1]

        result_maze = ""
        for i in range(len(maze)):
            for j in range(len(maze[0])):
                result_maze = result_maze + maze[i][j]
            result_maze = result_maze + '\n'

        animation.append(result_maze)

    #animate
    for index in range(0, len(animation)):
        sys.stdout.write(str(animation[index]) + "\r")
        sys.stdout.flush()
        time.sleep(0.2)


###########################################
