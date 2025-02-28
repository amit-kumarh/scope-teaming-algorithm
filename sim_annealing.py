import pandas as pd
import numpy as np
import random
from response_generator.names import SCOPE_TEAMS

class Solution:
    def __init__(self, responses, teams=None):
        self.responses = responses
        if teams is not None:
            self.teams = teams
        else:
            self.teams = self.gen_random_teams()

    def total_rating(self):
        ans = 0
        for student, team in self.teams.items():
            ans += self.responses.loc[self.responses["Name"] == student][team].values[0]
        return ans

    def heuristic(self):
        return self.total_rating()

    def swap_two(self, s1, s2):
        self.teams[s1], self.teams[s2] = self.teams[s2], self.teams[s1]
    
    def swapped_heuristic(self, s1, s2):
        self.swap_two(s1, s2)
        h = self.heuristic()
        self.swap_two(s1, s2)
        return h

    def gen_random_teams(self):
        teams = {}
        ppl_list = np.random.permutation(self.responses["Name"])
        for i, student in enumerate(ppl_list):
            teams[student] = SCOPE_TEAMS[i // 5]
        # print(teams)
        return teams
    


def boltzmann(delta, k, T):
    return np.exp(-delta / (k * T))

def anneal(curr_solution, T0, alpha):
    T = T0

    best_solution = curr_solution
    best_heuristic = 0

    while T > 0.001:
        s1 = random.choice(list(curr_solution.teams.keys()))
        s2 = random.choice(list(curr_solution.teams.keys()))
        delta = (ch := curr_solution.swapped_heuristic(s1, s2)) - curr_solution.heuristic()
        if delta > 0 or np.random.rand() < boltzmann(delta, 1e-23, T):
            curr_solution.swap_two(s1, s2)
            if ch > best_heuristic:
                best_solution = curr_solution
                best_heuristic = ch
        
        print(curr_solution.heuristic())
        T *= alpha
    
    return best_solution, best_heuristic


def main():
    T0 = 1
    alpha = 0.99

    responses = pd.read_csv('responses.csv')
    initial = Solution(responses)
    print('best:', anneal(initial, T0, alpha)[1])
    

if __name__ == '__main__':
    main()
