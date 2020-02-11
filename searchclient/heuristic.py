from abc import ABCMeta, abstractmethod
import math
from collections import deque
from typing import List
from state import State


class Heuristic(metaclass=ABCMeta):
    goal_x = None
    goal_y = None

    def __init__(self, initial_state: 'State'):
        # Here's a chance to pre-process the static parts of the level.
        rows = len(initial_state.goals)
        cols = len(initial_state.goals[0])

        self.walls = initial_state.walls

        for i in range(rows):
            for j in range(cols):
                goals_field = initial_state.goals[i][j]

                if goals_field is not None:
                    Heuristic.goal_x = i
                    Heuristic.goal_y = j

    def shortest_path_between_source_and_goals(self, start_state: State, goal_states: List[State]) -> dict:
        """
        Method calculating the distance between source (start_state) and all goals from goal_states list.
        It shall be used for calculating distances between tiles and boxes/goals.
        """
        # point has (x_cord, y_cord, dist_from_source)
        queue = deque()
        visited = self.walls
        start = (start_state.agent_row, start_state.agent_col, 0)
        visited[start[0]][start[1]] = True

        queue.append(start)

        goal_distance_dict = {}

        while len(queue) > 0:
            curr = queue.pop()

            for goal_state in goal_states:
                if curr[0] == goal_state.agent_row and curr[1] == goal_state.agent_col:
                    goal_distance_dict[State.goals[curr[0]], State.goals[curr[1]]] = curr[2]

                # top
                top_neighbour = (curr[0], curr[1] - 1, curr[2] + 1)
                bot_neighbour = (curr[0], curr[1] + 1, curr[2] + 1)
                left_neighbour = (curr[0] - 1, curr[1], curr[2] + 1)
                right_neighbour = (curr[0] + 1, curr[1], curr[2] + 1)

                neighbours = [top_neighbour, bot_neighbour, left_neighbour, right_neighbour]

                for neighbour in neighbours:
                    if 0 <= neighbour[0] < len(self.walls) and 0 <= neighbour[1] < len(self.walls[0]):
                        if visited[neighbour[0]][neighbour[1]] is None:
                            visited[neighbour[0]][neighbour[1]] = True
                            queue.append()

        return goal_distance_dict









    # TODO: better heuristic. Also aknowledge multiple goals and having boxes
    # idea: take the distance to box X, goal x and get the sum. Go to the box with the lowest sum
    # TODO: method for calculating shortest path with aknowledginthe walls
    def h(self, state: 'State') -> 'int':
        goals = State.goals[Heuristic.goal_x][Heuristic.goal_y]
        test = self.shortest_path_between_source_and_goals(state, goals)
        x_diff = abs(state.agent_row - Heuristic.goal_x)
        y_diff = abs(state.agent_col - Heuristic.goal_y)
        # estimated cost of reaching a goal from state
        return x_diff + y_diff

    @abstractmethod
    def f(self, state: 'State') -> 'int': pass

    @abstractmethod
    def __repr__(self): raise NotImplementedError


class AStar(Heuristic):
    def __init__(self, initial_state: 'State'):
        super().__init__(initial_state)

    def f(self, state: 'State') -> 'int':
        return state.g + self.h(state)

    def __repr__(self):
        return 'A* evaluation'


class WAStar(Heuristic):
    def __init__(self, initial_state: 'State', w: 'int'):
        super().__init__(initial_state)
        self.w = w
    
    def f(self, state: 'State') -> 'int':
        return state.g + self.w * self.h(state)
    
    def __repr__(self):
        return 'WA* ({}) evaluation'.format(self.w)


class Greedy(Heuristic):
    def __init__(self, initial_state: 'State'):
        super().__init__(initial_state)
    
    def f(self, state: 'State') -> 'int':
        return self.h(state)
    
    def __repr__(self):
        return 'Greedy evaluation'

