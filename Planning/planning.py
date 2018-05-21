#This class implements planning using A* - mp1.1
#find the factory sequence with the smallest number of miles traveled.
#State: Save each state with the current position of the truck and
#the remaining components of each widget using tuple.
#e.g. state = (curr_place, w1, w2, w3, w4, w5)
#where w1, w2, w3, w4, w5 are tuples of the remaining factories of each widget.
#Heuristic: mst of the remaining components.
#This heursitic is admissible because for different components remaining, the
#the truck has to at least travel all of the remaining components.

__author__ = "chongye Wang"

from heapq import heappush, heappop
import sys

def remaining_place(curr_place, w1, w2, w3, w4, w5):

    dict = {}
    list = [w1,w2, w3, w4, w5]
    for w in list:
        for char in w:
            if char not in dict:
                dict[char] = 0
            dict[char] += 1
    if curr_place in dict:
        return len(dict) - 1
    else:
        return len(dict)

def mst(distance, w1, w2, w3, w4, w5):
    """
    This method implements the mst serving as heuristic.
    """
    dict = {}
    list = [w1, w2, w3, w4, w5]
    for w in list:
        for char in w:
            if char not in dict:
                dict[char] = 0
            dict[char] += 1

    place_list = [x for x in dict]

    if not place_list: return 0

    print(place_list)

    visited = []
    visited.append(place_list[0])
    place_list.pop(0)

    minimum = 0

    while len(place_list) != 0:
        curr_min = sys.maxsize
        remove = 0
        for v in visited:
            for uv in place_list:
                d = distance[(v, uv)]
                if d < curr_min:
                    curr_min = d
                    remove = uv
        minimum += curr_min
        visited.append(remove)
        place_list.remove(remove)

    return minimum

def Astar(distance, w1, w2, w3, w4, w5):

    g_value = {}
    f_value = {}

    start_state = []
    start_state.append('S')
    start_state.append(tuple(w1[:]))
    start_state.append(tuple(w2[:]))
    start_state.append(tuple(w3[:]))
    start_state.append(tuple(w4[:]))
    start_state.append(tuple(w5[:]))

    start_state = tuple(start_state)

    g_value[start_state] = 0
    f_value[start_state] = mst(distance, w1, w2, w3, w4, w5)

    goal_state = []
    for goal in ['A', 'B', 'C', 'D', 'E']:
        goal_state.append((goal, (), (), (), (), ()))

    frontier = []
    heappush(frontier, (f_value[start_state], start_state))

    visited = {}

    while len(frontier) != 0:

        curr_state = heappop(frontier)[1]
        print(curr_state)

        #current place of truck
        curr_place = curr_state[0]

        visited[curr_state] = 1

        if curr_state[1:6] == ((), (), (), (), ()):
            return g_value[curr_state]

        for index in range(1, 6):
            if not curr_state[index]: continue
            front_place = curr_state[index][0]

            new_widget_condition = list(curr_state[1:6])
            new_widget_condition[index - 1] = new_widget_condition[index - 1][1:]

            #new state : [curr_place, w1, w2, w3, w4, w5]
            new_state = []
            new_state.append(front_place)
            new_state.extend(new_widget_condition)
            new_state = tuple(new_state)
            print(new_state)

            if new_state not in visited:
                visited[new_state] = 0
            if visited[new_state] == 1:
                continue

            if new_state not in g_value:
                #stay at the same place, keep original g_value
                if curr_place == front_place:
                    g_value[new_state] = g_value[curr_state]
                else:
                    g_value[new_state] = g_value[curr_state] + distance[(curr_place, front_place)]
                f_value[new_state] = g_value[new_state] + mst(distance, new_state[1], new_state[2], new_state[3], new_state[4], new_state[5])
            else:
                new_g_value = 0
                #stay at the same place, keep original g_value
                if curr_place == front_place:
                    new_g_value = g_value[curr_state]
                else:
                    new_g_value = g_value[curr_state] + distance[(curr_place, front_place)]
                if new_g_value < g_value[new_state]:
                    g_value[new_state] = new_g_value
                    f_value[new_state] = g_value[new_state] + mst(distance, new_state[1], new_state[2], new_state[3], new_state[4], new_state[5])

            if new_state not in frontier:
                heappush(frontier, (f_value[new_state], new_state))



if __name__ == "__main__":

    widget1 = ['A', 'E', 'D', 'C', 'A']
    widget2 = ['B', 'E', 'A', 'C', 'D']
    widget3 = ['B', 'A', 'B', 'C', 'E']
    widget4 = ['D', 'A', 'D', 'B', 'D']
    widget5 = ['B', 'E', 'C', 'B', 'D']

    distance = {}
    distance[('A', 'A')] = 0
    distance[('B', 'B')] = 0
    distance[('C', 'C')] = 0
    distance[('D', 'D')] = 0
    distance[('E', 'E')] = 0
    distance[('A', 'S')] = 0
    distance[('S', 'A')] = 0
    distance[('B', 'S')] = 0
    distance[('S', 'B')] = 0
    distance[('C', 'S')] = 0
    distance[('S', 'C')] = 0
    distance[('D', 'S')] = 0
    distance[('S', 'D')] = 0
    distance[('E', 'S')] = 0
    distance[('S', 'E')] = 0

    distance[('A', 'B')] = 1064
    distance[('B', 'A')] = 1064
    distance[('A', 'C')] = 673
    distance[('C', 'A')] = 673
    distance[('A', 'D')] = 1401
    distance[('D', 'A')] = 1401
    distance[('A', 'E')] = 277
    distance[('E', 'A')] = 277

    distance[('B', 'C')] = 958
    distance[('C', 'B')] = 958
    distance[('B', 'D')] = 1934
    distance[('D', 'B')] = 1934
    distance[('B', 'E')] = 337
    distance[('E', 'B')] = 337

    distance[('C', 'D')] = 1001
    distance[('D', 'C')] = 1001
    distance[('C', 'E')] = 399
    distance[('E', 'C')] = 399

    distance[('D', 'E')] = 387
    distance[('E', 'D')] = 387

    Astar(distance, widget1, widget2, widget3, widget4, widget5)
