import pandas as pd
import numpy as np
import random
from matplotlib import pyplot as plt


from response_generator.names import SCOPE_TEAMS

import argparse

def parse_arguments():
    """
    Parses command-line arguments for a local search teaming algorithm.
    """
    parser = argparse.ArgumentParser(description="Local Search Teaming Algorithm")
    subparsers = parser.add_subparsers(dest="mode", help="Choose between single run or parameter sweep")

    # Single run mode
    single_run_parser = subparsers.add_parser("single", help="Run the algorithm with specific parameters")
    single_run_parser.add_argument("--alpha", type=float, help="Alpha parameter", required=True)
    single_run_parser.add_argument("--threshold", type=float, help="Threshold parameter", required=True)

    # Parameter sweep mode
    sweep_parser = subparsers.add_parser("sweep", help="Run the algorithm with a range of parameters")
    sweep_parser.add_argument("--alpha_start", type=float, help="Start value for alpha sweep")
    sweep_parser.add_argument("--alpha_end", type=float, help="End value for alpha sweep")
    sweep_parser.add_argument("--alpha_step", type=float, help="Step size for alpha sweep")

    # Optional arguments, common to both modes.
    parser.add_argument("--seed", type=int, help="Random seed for reproducibility")

    return parser.parse_args()

class Solution:
    def __init__(self, responses, teams=None):
        self.responses = responses
        self.teams = teams if teams is not None else self.gen_random_teams()

    def total_rating(self):
        """
        Total the project ratings for this solution
        """
        ans = 0
        for student, team in self.teams.items():
            ans += self.responses.loc[self.responses["Name"] == student][team].values[0]
        return ans

    def antiprefs_violated(self):
        """
        Return the number of silver bullet violations in this solution
        """
        ret = 0
        for student, team in self.teams.items():
            antiprefs = self.responses.loc[self.responses["Name"] == student]["Antipreferences"].values[0]
            for a in antiprefs:
                if self.teams[a] == team:
                    ret += 1
        return ret


    def heuristic(self):
        return self.total_rating() - 100 * self.antiprefs_violated()

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
    
def boltzmann(delta, T):
    k = 1e-23
    return np.exp(delta / (k * T))

def anneal(curr_solution, T0, alpha, thresh):
    T = T0

    best_solution = curr_solution
    best_heuristic = 0

    while T > thresh:
        s1 = random.choice(list(curr_solution.teams.keys()))
        s2 = random.choice(list(curr_solution.teams.keys()))
        delta = (ch := curr_solution.swapped_heuristic(s1, s2)) - curr_solution.heuristic()
        if delta > 0 or np.random.rand() < boltzmann(delta, T):
            curr_solution.swap_two(s1, s2)
            if ch > best_heuristic:
                best_solution = curr_solution
                best_heuristic = ch
        
        T *= alpha
    return best_solution, best_heuristic


def main():
    T0 = 1
    THRESHOLD = 0.001
    args = parse_arguments()

    responses = pd.read_json('responses.json')

    if args.mode == "single":
        random.seed(args.seed)
        np.random.seed(args.seed)
        solution = Solution(responses)
        _best_solution, best_heuristic = anneal(solution, T0, args.alpha, THRESHOLD)
        print(best_heuristic)
    elif args.mode == "sweep":
        # parameter sweep alpha and plot results
        alphas = np.arange(args.alpha_start, args.alpha_end, args.alpha_step)
        results = []
        for alpha in alphas:
            random.seed(args.seed)
            np.random.seed(args.seed)
            solution = Solution(responses)
            _best_solution, best_heuristic = anneal(solution, T0, alpha, THRESHOLD)
            results.append(best_heuristic)
            print(f"Alpha: {alpha}, Heuristic: {best_heuristic}")

        plt.plot(alphas, results)
        plt.xlabel("Alpha")
        plt.ylabel("Best Heuristic")
        plt.title("Alpha Sweep")
        plt.show()

if __name__ == '__main__':
    main()
