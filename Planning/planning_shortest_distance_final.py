#This class implements planning using A* - mp1.1
#find the factory sequence with the smallest number of miles traveled.
#State: Save each state with the current position of the truck and
#the remaining components of each widget using tuple.
#e.g. state = (curr_place, w1, w2, w3, w4, w5)
#where w1, w2, w3, w4, w5 are tuples of the remaining factories of each widget.
#Heuristic: find the shortest distance between the current remaining place
#and the shortest distance between this place and any other places
#This heursitic is admissible and consistent

__author__ = "Chongye Wang"

import sys
from heapq import heappush, heappop

def Astar(distance, w1, w2, w3, w4, w5):
    """
    This function implements the Astar of
    planning search with shortest distance
    """

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

    node_expanded = 0;

    while len(frontier) != 0:

        curr_state = heappop(frontier)[1]

        #current place of truck
        curr_place = curr_state[0]

        visited[curr_state] = 1

        node_expanded += 1

        if curr_state[1:6] == ((), (), (), (), ()):
            return g_value[curr_state], node_expanded

        for component in ['A', 'B', 'C', 'D', 'E']:

            new_widget_condition = list(curr_state[1:6])
            for index in range(1, 6):
                if not curr_state[index]: continue
                if curr_state[index][0] == component:
                    new_widget_condition[index - 1] = new_widget_condition[index - 1][1:]
            if new_widget_condition == list(curr_state[1:6]): continue


            #new state : [curr_place, w1, w2, w3, w4, w5]
            new_state = []
            new_state.append(component)
            new_state.extend(new_widget_condition)
            new_state = tuple(new_state)

            if new_state not in visited:
                visited[new_state] = 0
            if visited[new_state] == 1:
                continue

            if new_state not in g_value:
                #stay at the same place, keep original g_value
                if curr_place == component:
                    g_value[new_state] = g_value[curr_state]
                else:
                    g_value[new_state] = g_value[curr_state] + get_two_point_distance(distance, curr_place, component)
                f_value[new_state] = g_value[new_state] + mst(distance, new_state[1], new_state[2], new_state[3], new_state[4], new_state[5])
            else:
                new_g_value = 0
                #stay at the same place, keep original g_value
                if curr_place == component:
                    new_g_value = g_value[curr_state]
                else:
                    new_g_value = g_value[curr_state] + get_two_point_distance(distance, curr_place, component)
                if new_g_value < g_value[new_state]:
                    g_value[new_state] = new_g_value
                    f_value[new_state] = g_value[new_state] + mst(distance, new_state[1], new_state[2], new_state[3], new_state[4], new_state[5])

            if new_state not in frontier:
                heappush(frontier, (f_value[new_state], new_state))


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
                d = get_two_point_distance(distance, v, uv)
                if d < curr_min:
                    curr_min = d
                    remove = uv
        minimum += curr_min
        visited.append(remove)
        place_list.remove(remove)

    return minimum


def heuristic(distance, w1, w2, w3, w4, w5):

    """
    This method implements the heuristic.
    """
    dict = {}
    list = [w1, w2, w3, w4, w5]
    for w in list:
        for char in w:
            if char not in dict:
                dict[char] = 0
            dict[char] += 1

    place_list = [x for x in dict]
    print(place_list)
    #return 0;

    if not place_list or len(place_list) == 1: return 0

    print(place_list)

    curr_min = sys.maxsize

    orig_list = ['A', 'B', 'C', 'D', 'E']
    for place in place_list:
        for orig in orig_list:
            if place != orig:
                d = distance[(place, orig)]
                if d < curr_min:
                    curr_min = d
    return curr_min


def get_two_point_distance(distance, place1, place2):

    g_value = {}
    f_value = {}

    g_value[place1] = 0
    f_value[place1] = 0


    frontier = []
    heappush(frontier, (f_value[place1], place1))

    visited = {}

    while len(frontier) != 0:

        curr_state = heappop(frontier)[1]

        visited[curr_state] = 1

        if curr_state == place2:
            return g_value[curr_state]

        for component in ['A', 'B', 'C', 'D', 'E']:
            if component not in visited:
                visited[component] = 0
            if visited[component] == 1:
                continue
            score = g_value[curr_state] + distance[(curr_state, component)]
            if component not in g_value:
                g_value[component] = score
                f_value[component] = score
            else:
                if score < g_value[component]:
                    g_value[component] = score
                    f_value[component] = score
            if component not in frontier:
                heappush(frontier, (f_value[component], component))




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


    distance, node_expanded = Astar(distance, widget1, widget2, widget3, widget4, widget5)
    print(distance)#5473
    print(node_expanded)#21115
