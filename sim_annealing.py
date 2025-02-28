import pandas as pd
import numpy as np
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

    def gen_random_teams(self):
        teams = {}
        ppl_list = np.random.permutation(self.responses["Name"])
        for i, student in enumerate(ppl_list):
            teams[student] = SCOPE_TEAMS[i // 5]
        print(teams)
        return teams

def main():
    responses = pd.read_csv('responses.csv')
    initial = Solution(responses)
    print(initial.total_rating())

if __name__ == '__main__':
    main()
