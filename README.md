# SCOPE Teaming Algorithm

Team Members: Amit Kumar-Hermosillo, Lily Jiang

## Technical Write Up

### Background of Algorithm (~1-2 paragraphs)

This implementation relies on Simulated Annealing, which is a metaheuristic inspired by annealing in metallurgy (a process that involves heating a metal to a high temperature and slowly cooling it down to remove defects in its crystal structure). The algorithm starts at a "high temperature", meaning it is more willing to accept a random solution that is worse than the current solution so it explores a wide range of solutions. As the algorithm "cools down", it becomes less willing to accept worse solutions, allowing it to converge to a solution. Because of this mechanic, this algorithm is better at handling complex, multi-peaked solution spaces than simpler algorithms like local searches, which easily get stuck in a local optima. Compared to other metaheuristics like genetic algorithms or ant colonies, simulated annealing is simpler to refine as it requires tweaking of only one or two parameters (the cooling rate and/or the threshold for when to stop iterating). However, despite all of it benefits, simulated annealing is not guaranteed to find the exact optimal solution and thus falls short when a precise solution is required.

The main design decisions with simulated annealing stem from the parameter values. **Alpha**, the cooling rate, determines how quickly the algorithm will converge to a solution. A low alpha like 0.8 causes the algorithm to converge quickly, but is more likely to not find the optimal solution. A high alpha like 0.99 allows the algorithm to explore more of the solution space (due to its influence on the Boltzmann constant), but takes much longer to converge and uses more computing power. The **threshold** for stopping the algorithm is the other important parameter. A high threshold may cause the algorithm to not converge to a solution. A low threshold may cause the algorithm to take too long to converge.

### How it Works (Walkthrough)
* How does it work? What components are in its design?
* What are its operating principles? What is the intuition behind its operating principles?
* Original figures/diagrams to aid explanation

### Solving a Problem (~1-2 paragraphs)
* Choose an application that your algorithm can be applied to & explain it
* Discuss how the algorithm would be applied/adapted to the problem as presented
    * Are there alterations that need to be made to the algorithm to enable it to be applied to this problem?
    * Are there key assumptions about the problem that must hold true in order to use this algorithm?
* Other use cases of the algorithm

We have chosen to adapt the simulated annealing algorithm to the problem of SCOPE team allocation at Olin - in other words, allocating a set of students into teams with various priorities and factors at play that aren't solvable at a glance in a most optimal fashion. This includes things like student wishlists for project, team antipreferences, required majors and skillsets, citizenship requirements, etc.

We have adapted the simulated annealing algorithm to this problem as follows:
- A single solution would be any allocation of the students onto teams (for this codebase, we are going with 65 students and 13 teams of 5 students each). This would make the solution space all of those possible allocations.
- Our heuristic function at the moment incorporates two factors.
    - The first is the student project rating; each student rates each project on a scale from 1-5, and project "score" of a particular solution is simply the sum of each student's score for their assigned project
    - Any violated antipreferences subtract 100 from that solution's score. We chose this number because we wanted the penalty to be harsh, such that most of the time a violated antipreference is much worse than lower project enjoyment, but doesn't entirely disqualify them if they are the only viable option
    - As more constraints and elements were to be added to this teaming algorithm, the heuristic could be adjusted to include those.
- Our neighbor relation is simply swapping two students around so they are on each other's teams.

As far as simulated annealing-specific parameters, we've set:

- The initial system temperature to 1
- The stop criteria as when the system temperature drops below 0.001
- The cooling schedule as $T_{i+1} = T_i * \alpha$, and swept alpha from 0.8 to 0.99 to evaluate the trade-off between iterations (and therefore runtime) vs performance.

In `//reponse_generation`, there's a quick script that generates survey reponses which are then used to test this algorithm in the remainder of our codebase.

As far as other applications, simulated annealing is a very common local search variant, and is typically employed in difficult problems where it might be impossible to find a most optimal solution through brute force, including image processing and computer vision, circuit design/VLSI layout, and other kinds of resource allocation problems.

### Ethical Analysis (~1-2 Paragraphs)

There are ethical dilemmas when using algorithms like this to create student SCOPE teams. For one, there are definite potential sources of bias, whether in the student responses or in the algorithm's heuristics, which might favor certain qualities that benefit some groups over others. There can also be a lack of transparency and privacy concerns regarding how student data is used, and students may feel a lack of agency or that insufficient care was put into their team selection. For instance, our algorithm has several random elements regarding how it traverses the solution space that could potentially have a major influence on the results.

Nevertheless, there are measures that can be taken to address these concerns (many of which are employed by the SCOPE teaching team!). Promoting transparency about the algorithm and the qualities it prioritizes can help reduce the "black box" feeling and increase students' sense of agency. Additionally, transparency into the factors the algorithm considers and prioritizes, and careful consideration of those factors, can help reduce algorithmic bias. Lastly, because there are factors that the algorithm simply cannot fully consider, adding human oversight and intervention is critical – an algorithm-assisted, but ultimately human, process as opposed to an entirely machine-driven one. 

## Libraries Used

numpy
pandas
random
matplotlib
collections
argparse

## Resources Used

Lecture Slides
[SCOPE Teaming Algorithm](https://github.com/AllenDowney/TeamAllocation)
[Geeks For Geeks](https://www.geeksforgeeks.org/simulated-annealing/)

