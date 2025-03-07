import pandas as pd
import numpy as np
import random
from matplotlib import pyplot as plt
from collections import defaultdict

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
    parser.add_argument("--iterations", type=int, help="Random seed for reproducibility")

    return parser.parse_args()


class Solution:
    def __init__(self, responses, teams=None):
        '''
        Initializes a solution object with a given set of responses and teams.
        If no teams are provided, generates random teams.
        '''
        self.responses = responses
        self.teams = teams if teams is not None else self.gen_random_teams()

    def total_rating(self):
        """
        Total the students' project ratings for the current teams they're assigned to.

        Returns: an int representing the total project rating for the solution.
        """
        ans = 0
        for student, team in self.teams.items():
            ans += self.responses.loc[self.responses["Name"] == student][team].values[0]
        return ans

    def antiprefs_violated(self):
        """
        Counts the number of silver bullet violations in this solution.

        Returns: an int representing the number of silver bullet violations.
        """
        ret = 0
        for student, team in self.teams.items():
            antiprefs = self.responses.loc[self.responses["Name"] == student]["Antipreferences"].values[0]
            for a in antiprefs:
                if self.teams[a] == team:
                    ret += 1
        return ret

    def heuristic(self):
        """
        Heuristic function for the solution.

        Returns: an int representing the heuristic value of the solution.
        """
        return self.total_rating() - 100 * self.antiprefs_violated()

    def swap_two(self, s1, s2):
        '''
        Swaps the teams of two specified students.
        
        Args:
            s1 (str): the name of the first student
            s2 (str): the name of the second student
        '''
        self.teams[s1], self.teams[s2] = self.teams[s2], self.teams[s1]
    
    def swapped_heuristic(self, s1, s2):
        '''
        Checks the heuristic value of the solution if two students swap
        teams (while still preserving the original teams).

        Args:
            s1 (str): the name of the first student
            s2 (str): the name of the second student

        Returns: an int representing the heuristic value of the solution
            if the teams of two specified students are swapped.
        '''
        self.swap_two(s1, s2)
        h = self.heuristic()
        self.swap_two(s1, s2)
        return h

    def gen_random_teams(self):
        '''
        Generates random teams for the students in the response data.

        Returns: a dictionary mapping student names to their assigned team names.
        '''
        teams = {}
        ppl_list = np.random.permutation(self.responses["Name"])
        for i, student in enumerate(ppl_list):
            teams[student] = SCOPE_TEAMS[i // 5]
        return teams


def boltzmann(delta, T):
    '''
    Boltzmann probability function for simulated annealing.

    Args:
        delta (int): the change in heuristic value
        T (float): the current temperature

    Returns: a float representing the probability of accepting the new solution
    '''
    k = 20
    return np.exp(delta / (k * T))


def anneal(curr_solution, T0, alpha, thresh):
    '''
    Simulated annealing algorithm for teaming.

    Args:
        curr_solution (Solution): the initial solution
        T0 (int or float): the initial temperature
        alpha (float): the cooling rate
        thresh (float): the stopping threshold

    Returns: a tuple containing the best solution found (Solution)
        and its heuristic value (int)
    '''
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


def anneal_with_visual(curr_solution, T0, alpha, thresh):
    '''
    Simulated annealing algorithm for teaming with visualizations.

    Writes the best solution found to a file `best_solution.txt`, including
    the heuristic value, total rating, antiprefs violated, and teams.

    Plots the current heuristic and best heuristic over annealing iterations.

    Args:
        curr_solution (Solution): the initial solution
        T0 (int or float): the initial temperature
        alpha (float): the cooling rate
        thresh (float): the stopping threshold
    '''
    T = T0

    best_solution = curr_solution
    best_heuristic = 0

    heuristics_curr = []
    heuristics_best = []

    while T > thresh:
        s1 = random.choice(list(curr_solution.teams.keys()))
        s2 = random.choice(list(curr_solution.teams.keys()))
        delta = (ch := curr_solution.swapped_heuristic(s1, s2)) - curr_solution.heuristic()
        if delta > 0 or np.random.rand() < boltzmann(delta, T):
            curr_solution.swap_two(s1, s2)
            if ch > best_heuristic:
                best_solution = curr_solution
                best_heuristic = ch
            heuristics_curr.append(ch)
            heuristics_best.append(best_heuristic)
        
        T *= alpha

    teams = {}

    for team in SCOPE_TEAMS:
        teams[team] = []

    for student, team in best_solution.teams.items():
        teams[team].append(student)

    with open("best_solution.txt", "w") as f:
        f.write(f"\Heuristic: {str(best_heuristic)}")
        f.write(f"\nTotal Rating: {best_solution.total_rating()}")
        f.write(f"\nAntiprefs Violated: {best_solution.antiprefs_violated()}\n")

    with open("best_solution.txt", "a") as f:
        for team, students in teams.items():
            f.write(f"\n{team}: {', '.join(students)}")

    print("Best Solution Written to best_solution.txt")

    plt.figure(1)
    plt.plot(range(len(heuristics_curr)), np.array(heuristics_curr))
    plt.xlabel("Iteration Number")
    plt.ylabel("Current Heuristic")
    plt.title("Current Heuristic vs. Alpha Over Iterations")
    plt.ylim((-300, 300))

    plt.figure(2)
    plt.plot(range(len(heuristics_best)), np.array(heuristics_best))
    plt.xlabel("Iteration Number")
    plt.ylabel("Current Best Heuristic")
    plt.title("Best Heuristic vs. Alpha Over Iterations")
    plt.ylim((-300, 300))
    plt.show()


def sweep_alpha(T0, alpha, thresh):
    '''
    Sweeps the alpha parameter for the simulated annealing algorithm.

    Writes the results of the sweep to a CSV file `alpha_sweep.csv`, and
    plots the average heuristic for each alpha tested.

    Args:
        T0 (int or float): the initial temperature
        alpha (float): the cooling rate
        thresh (float): the stopping threshold
    '''
    args = parse_arguments()

    responses = pd.read_json('responses.json')

    if args.mode == "single":
        if args.seed is not None:
            random.seed(args.seed)
            np.random.seed(args.seed)
        solution = Solution(responses)
        _best_solution, best_heuristic = anneal(solution, T0, args.alpha, thresh)
        print(best_heuristic)
    elif args.mode == "sweep":
        # parameter sweep alpha and plot results
        alphas = np.arange(args.alpha_start, args.alpha_end+args.alpha_step, args.alpha_step)
        all_results = defaultdict(list)

        with open("alpha_sweep.csv", "w") as f:
            f.write("alpha,run,heuristic\n")

        for alpha in alphas:
            alpha = round(alpha, 2)
            for _ in range(args.iterations):
                if args.seed is not None:
                    random.seed(args.seed)
                    np.random.seed(args.seed)
                solution = Solution(responses)
                _best_solution, best_heuristic = anneal(solution, T0, alpha, thresh)
                all_results[alpha].append(best_heuristic)
                print(f"Alpha: {alpha}, Heuristic: {best_heuristic}")

            # Write to CSV
            with open("alpha_sweep.csv", "a") as f:
                for run, heuristic in enumerate(all_results[alpha]):
                    f.write(f"{alpha},{run},{heuristic}\n")

        # Plot average best for funsies
        plt.plot(alphas, [np.mean(all_results[round(alpha, 2)]) for alpha in alphas])
        plt.xlabel("Alpha")
        plt.ylabel("Average Best Heuristic")
        plt.title("Alpha Sweep")
        plt.show()


def main():
    T0 = 1
    THRESHOLD = 0.001
    responses = pd.read_json('responses.json')

    # CODE FOR ANNEALING
    # anneal(Solution(responses), T0, 0.99, THRESHOLD)

    # CODE FOR ANNEALING WITH VISUAL
    anneal_with_visual(Solution(responses), T0, 0.99, THRESHOLD)

    # CODE TO RUN ANNEALING SWEEP
    # sweep_alpha(T0, 0.99, THRESHOLD)

if __name__ == '__main__':
    main()
