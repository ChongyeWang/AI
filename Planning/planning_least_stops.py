#This class implements planning using A* - mp1.1
#find the factory sequence with the smallest number of miles traveled.
#(the smallest number of factories visited).
#State: Save each state with the current position of the truck and
#the remaining components of each widget using tuple.
#e.g. state = (curr_place, w1, w2, w3, w4, w5)
#where w1, w2, w3, w4, w5 are tuples of the remaining factories of each widget.
#Heuristic: the number of remaining places of components.
#This heursitic is admissible because for different components that are
#currently not at the same place with the truck, the truck has at least to
#reach all of these remaining components.

__author__ = "Chongye Wang"


from heapq import heappush, heappop

def remaining_place(curr_place, w1, w2, w3, w4, w5):
    """
    This method check the number of remaining types
    of components.
    """
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

def Astar(w1, w2, w3, w4, w5):
    """
    This fucntion implements the planning search with
    A* with remaining_place function as heursitic.
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
    f_value[start_state] = remaining_place('S', w1, w2, w3, w4, w5)

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

            if new_widget_condition == list(curr_state[1:6]): continue #no change, continue to next component

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
                    g_value[new_state] = g_value[curr_state] + 1
                f_value[new_state] = g_value[new_state] + remaining_place(component, new_state[1], new_state[2], new_state[3], new_state[4], new_state[5])
            else:
                new_g_value = 0
                #stay at the same place, keep original g_value
                if curr_place == component:
                    new_g_value = g_value[curr_state]
                else:
                    new_g_value = g_value[curr_state] + 1
                if new_g_value < g_value[new_state]:
                    g_value[new_state] = new_g_value
                    f_value[new_state] = g_value[new_state] + remaining_place(component, new_state[1], new_state[2], new_state[3], new_state[4], new_state[5])

            if new_state not in frontier:
                heappush(frontier, (f_value[new_state], new_state))


if __name__ == "__main__":
    widget1 = ['A', 'E', 'D', 'C', 'A']
    widget2 = ['B', 'E', 'A', 'C', 'D']
    widget3 = ['B', 'A', 'B', 'C', 'E']
    widget4 = ['D', 'A', 'D', 'B', 'D']
    widget5 = ['B', 'E', 'C', 'B', 'D']

    step, node_expanded = Astar(widget1, widget2, widget3, widget4, widget5)
    print(step)#11
    print(node_expanded)#2290
