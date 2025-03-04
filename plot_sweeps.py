import numpy as np
from matplotlib import pyplot as plt


def heuristic_vs_alpha(alpha, heuristic):
    """
    Scatter plot of the heuristic against the alpha parameter
    """
    jitter_strength = 0.002
    alpha_jittered = alpha + np.random.normal(0, jitter_strength, size=alpha.shape)
    heuristic_jittered = heuristic + np.random.normal(0, jitter_strength, size=heuristic.shape)

    plt.scatter(alpha_jittered, heuristic_jittered, alpha=0.5, s=20)
    plt.title('Heuristic vs Alpha')
    plt.xlabel('Alpha')
    plt.ylabel('Heuristic')
    plt.show()


def main():
    filename = "alpha_sweep.csv"
    data = np.genfromtxt(filename, delimiter=',', skip_header=1)

    alpha = data[:, 0]
    run = data[:, 1]
    heuristic = data[:, 2]

    heuristic_vs_alpha(alpha, heuristic)

if __name__ == '__main__':
    main()
