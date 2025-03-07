import numpy as np
from matplotlib import pyplot as plt


def heuristic_vs_alpha(alpha, heuristic):
    """
    Scatter plot of the heuristic against the alpha parameter
    """
    jitter_strength = 0.002
    alpha_jittered = alpha + np.random.normal(0, jitter_strength, size=alpha.shape)

    plt.scatter(alpha_jittered, heuristic, alpha=0.5, s=20)
    plt.title('Allocation Strength by Cooling Schedule')
    plt.xlabel('Alpha')
    plt.ylabel('Heuristic Value')
    plt.savefig('media/alpha_sweep.png')
    plt.show()

def heuristic_vs_run(alpha, runs, heuristic):
    """
    Line plot of the heuristic against the alpha parameter for each run
    """
    plt.figure()
    for run in np.unique(runs):
        indices = np.where(runs == run)[0]
        
        alpha_run = alpha[indices]
        heuristic_run = heuristic[indices]
        
        sorted_indices = np.argsort(alpha_run)
        alpha_run_sorted = alpha_run[sorted_indices]
        heuristic_run_sorted = heuristic_run[sorted_indices]
        
        plt.plot(alpha_run_sorted, heuristic_run_sorted, marker='o', label=f'Run {run}')

    plt.title('Heuristic vs Alpha')
    plt.xlabel('Alpha')
    plt.ylabel('Heuristic')
    plt.legend(title="Run", loc="best")
    plt.show()


def main():
    filename = "alpha_sweep.csv"
    data = np.genfromtxt(filename, delimiter=',', skip_header=1)

    alpha = data[:, 0]
    run = data[:, 1]
    heuristic = data[:, 2]

    heuristic_vs_alpha(alpha, heuristic)
    # heuristic_vs_run(alpha, run, heuristic)

if __name__ == '__main__':
    main()
