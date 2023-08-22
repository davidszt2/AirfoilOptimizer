import pygad
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, rc
from IPython.display import HTML, Image
from PARSEC.Parsec import PARSECfoil
from BEZIER.Bezier import BEZIERfoil, listToCP


def runGA(gene_space, fitnessFunction, name):
    num_generations = 100
    num_parents_mating = 4
    num_genes = 11
    parent_selection_type = "sss"
    keep_parents = 2
    crossover_type = "single_point"
    mutation_type = "random"
    mutation_percent_genes = 10

    gene_space = [
        {'low': 0.01, 'high': 0.03},    # p1  - rLE Leading-edge radius
        {'low': 0.1, 'high': 0.7},      # p2  - XS Upper crest position in horizontal coordinates
        {'low': 0.03, 'high': 0.1},     # p3  - ZS Upper crest position in vertical coordinates
        {'low': -0.6, 'high': -0.2},    # p4  - ZXX,S Upper crest curvature
        {'low': 0.1, 'high': 0.7},      # p5  - XP Lower crest position in horizontal coordinates
        {'low': -0.03, 'high': -0.1},   # p6  - ZP Lower crest position in vertical coordinates
        {'low': 0.2, 'high': 0.6},      # p7  - ZXX,P Lower crest curvature
        {'low': 0, 'high': 0.025},      # p8  - ZT E Trailing-edge offset
        {'low': 0, 'high': 0.005},      # p9  - ∆ZT E Trailing-edge thickness
        {'low': -5, 'high': 5},         # p10 - αT E Trailing-edge direction
        {'low': 0, 'high': 5}           # p11 - βT E Trailing-edge wedge angle
    ]

    ga_instance = pygad.GA(num_generations=num_generations,
                           num_parents_mating=num_parents_mating,
                           fitness_func=fitnessFunction,
                           num_genes=num_genes,
                           sol_per_pop=50,
                           parent_selection_type=parent_selection_type,
                           keep_parents=keep_parents,
                           crossover_type=crossover_type,
                           mutation_type=mutation_type,
                           mutation_percent_genes=mutation_percent_genes,
                           gene_space=gene_space,
                           save_solutions=True)

    ga_instance.run()
    ga_instance.save(name)
    ga_instance.plot_fitness()
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    print("Parameters of the best solution : {solution}".format(solution=solution))
    print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
    print("Index of the best solution : {solution_idx}".format(solution_idx=solution_idx))


def animateGA(gaName, fileName, method):
    rc('animation', html='html5')

    ga_instance = pygad.load(gaName)

    solutionsArr = ga_instance.solutions

    """ANIMATION"""
    # Initial
    X, Y = PARSECfoil(solutionsArr[0]) if method == "PARSEC" else BEZIERfoil(listToCP(solutionsArr[0]), 16)
    fig, ax = plt.subplots()
    ax.set_xlim(( 0, 1))
    ax.set_ylim(( -0.5, 0.5))
    plt.gca().set_aspect('equal')
    line, = ax.plot([], [], lw=2)


    def init():
        line.set_data([], [])
        return (line,)


    def animate(i):
        X, Y = PARSECfoil(solutionsArr[i]) if method == "PARSEC" else BEZIERfoil(listToCP(solutionsArr[i]), 16)
        line.set_data(X, Y)
        plt.gca().set_aspect('equal')
        return (line,)


    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=len(solutionsArr), interval=20, blit=True)

    f = f"./{fileName}.gif"
    writergif = animation.PillowWriter(fps=30)
    anim.save(f, writer=writergif)
