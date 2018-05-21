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

def findPath(maze):
    """
    Find the solution of the maze(BFS)
    """
    queue = []
    start_Position = findStart(maze)
    queue.append(start_Position)

    #Get the width and height of maze
    width = len(maze[0])
    height = len(maze)
    size = width * height

    #Mark visited place
    visited = [0 for x in range(size)]

    #Keep track of the position of parent node
    parent_Position = [0 for x in range(width * height)]

    end_Position = 0
    while len(queue) != 0:
        curr = queue[len(queue) - 1]
        queue.pop(len(queue) - 1)
        currY = curr / width
        currX = curr % width
        visited[curr] = 1

        #Target Position finded
        if maze[currY][currX] == '.':
            end_Position = curr
            break

        #Left
        if currX - 1 >= 0 and maze[currY][currX - 1] != '%':
            if visited[curr - 1] != 1:
                queue.append(curr - 1)
                parent_Position[curr - 1] = curr
                #visited[curr - 1] = 1

        #Right
        if currX + 1 < width and maze[currY][currX + 1] != '%':
            if curr + 1 < size and visited[curr + 1] != 1:
                queue.append(curr + 1)
                parent_Position[curr + 1] = curr
                #visited[curr + 1] = 1

        #Up
        if currY - 1 >= 0 and maze[currY - 1][currX] != '%':
            if visited[curr - width] != 1:
                queue.append(curr - width)
                parent_Position[curr - width] = curr
                #visited[curr - width] = 1

        #Down
        if currY + 1 < height and maze[currY + 1][currX] != '%':
            if visited[curr + width] != 1:
                queue.append(curr + width)
                parent_Position[curr + width] = curr
                #visited[curr + width] = 1

    #Generate solution path
    position = end_Position
    while parent_Position[position] != start_Position:
        coordinate = parent_Position[position]
        maze[coordinate / width][coordinate % width] = '.'
        position = parent_Position[position]

    #Convert to String
    result = ""
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            result = result + maze[i][j]
        result = result + '\n'

    #Print the solution
    print(result)


width = 0
height = 0
infile = open('maze.txt', 'r')
for line in infile:
    width = len(line)
    height = height + 1

maze = [[0 for x in range(width)] for y in range(height)]
infile = open('maze.txt', 'r')
w = 0
h = 0
for line in infile:
    w = 0
    for c in line:
        if w < width:
            maze[h][w] = c
        w += 1
    h += 1

#Call function
findPath(maze)
