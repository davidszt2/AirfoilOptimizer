"""AIRFOIL OPTIMIZATION"""
# Author: David Moeller Sztajnbok
# Date:   July 2023

from PARSEC.Parsec import createPMatrix, PARSECfoil
from BEZIER.Bezier import BEZIERfoil, plotBEZIER, listToCP
import Airfoil
import GATools
import matplotlib.pyplot as plt
import numpy as np
import math
import os

import pygad

"""PARSEC EXAMPLE"""
# pArr = [
#     0.0130,     # p1  - rLE Leading-edge radius
#     0.2876,     # p2  - XS Upper crest position in horizontal coordinates
#     0.0566,     # p3  - ZS Upper crest position in vertical coordinates
#     -0.3951,    # p4  - ZXX,S Upper crest curvature
#     0.2127,     # p5  - XP Lower crest position in horizontal coordinates
#     -0.0290,    # p6  - ZP Lower crest position in vertical coordinates
#     0.2602,     # p7  - ZXX,P Lower crest curvature
#     0,          # p8  - ZT E Trailing-edge offset
#     0,          # p9  - ∆ZT E Trailing-edge thickness
#     -1.7939,    # p10 - αT E Trailing-edge direction
#     3.5879      # p11 - βT E Trailing-edge wedge angle
#     ]
#
# pMatrix = createPMatrix(pArr)
# X, Y = PARSECfoil(pMatrix)
#
# plt.plot(X, Y)
# plt.xlabel('x')
# plt.ylabel('y')
# plt.title("PARSEC Airfoil")
# plt.gca().set_aspect('equal')
# plt.show()
#
# try:
#     polar = Airfoil.runAirfoil(X, Y, "otherTest", 1e6, np.linspace(-5, 15, 21))
# except Exception as ex:
#     print(ex)
#
# foilPolar = Airfoil.createPolarDict(polar, "otherTest")
# print(foilPolar)

"""BEZIER EXAMPLE"""

# controlPoints = [
#     [1, 0.001],         # trailing edge (top)
#     [0.76, 0.08],
#     [0.52, 0.125],
#     [0.25, 0.12],
#     [0.1, 0.08],
#     [0, 0.03],          # leading edge (top)
#     [0, -0.03],         # leading edge (bottom)
#     [0.15, -0.08],
#     [0.37, -0.01],
#     [0.69, 0.04],
#     [1, -0.001]         # trailing edge (bottom)
# ]
#
# X, Y = BEZIERfoil(controlPoints, 16)
# plotBEZIER(X, Y, controlPoints)
#
# plt.show()

"""GENETIC ALGORITHM IMPLEMENTATION - GA PARSEC"""
# pArr = [
#     0.0130,     # p1  - rLE Leading-edge radius
#     0.2876,     # p2  - XS Upper crest position in horizontal coordinates
#     0.0566,     # p3  - ZS Upper crest position in vertical coordinates
#     -0.3951,    # p4  - ZXX,S Upper crest curvature
#     0.2127,     # p5  - XP Lower crest position in horizontal coordinates
#     -0.0290,    # p6  - ZP Lower crest position in vertical coordinates
#     0.2602,     # p7  - ZXX,P Lower crest curvature
#     0,          # p8  - ZT E Trailing-edge offset
#     0,          # p9  - ∆ZT E Trailing-edge thickness
#     -1.7939,    # p10 - αT E Trailing-edge direction
#     3.5879      # p11 - βT E Trailing-edge wedge angle
#     ]


def fitnessFunction(ga_instance, solution, solution_idx):
    # Run airfoil with solution and get aerodynamic parameters

    X, Y = PARSECfoil(solution)
    Re = 1e6
    alphaArray = np.linspace(-5, 15, 21)
    generationNum = ga_instance.generations_completed
    foilName = f"Gen{generationNum}Sol{solution_idx}"

    print(f"GENERATION {generationNum}\nSOLUTION: {solution_idx}")

    try:
        polar = Airfoil.runAirfoil(X, Y, foilName, Re, alphaArray)
        os.remove(f"./{foilName}.dat")
    except Exception as ex:
        print("EXCEPTION!")
        os.remove(f"./{foilName}.dat")
        return 0

    if len(polar['a']) < 0.25*len(alphaArray):
        print("TOO SHORT CONVERGENCE!!")
        return 0

    foilPolar = Airfoil.createPolarDict(polar, foilName)
    CLmax = Airfoil.getCLmax(foilPolar)
    LDmax = Airfoil.getLDmax(foilPolar)
    CDmin = Airfoil.getCDmin(foilPolar)
    LDmaxLOC = Airfoil.getLDmaxLOC(foilPolar)
    CDminLOC = Airfoil.getCDminLOC(foilPolar)

    fitness = LDmax

    print(f"FITNESS: {fitness}\n\n")

    if not math.isnan(fitness):
        return fitness
    else:
        return 0

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

# GATools.runGA(gene_space, fitnessFunction, 'test')
# GATools.animateGA('test', 'testAnimation', 'PARSEC')

"""GENETIC ALGORITHM IMPLEMENTATION - GA BEZIER"""
#
# def fitnessFunction(ga_instance, solution, solution_idx):
#     # Run airfoil with solution and get aerodynamic parameters
#     controlPoints = listToCP(solution)
#     X, Y = BEZIERfoil(controlPoints, 16)
#     Re = 1e6
#     alphaArray = np.linspace(-5, 15, 21)
#     generationNum = ga_instance.generations_completed
#     foilName = f"Gen{generationNum}Sol{solution_idx}"
#
#     print(f"GENERATION {generationNum}\nSOLUTION: {solution_idx}")
#
#     try:
#         polar = Airfoil.runAirfoil(X, Y, foilName, Re, alphaArray)
#         os.remove(f"./{foilName}.dat")
#     except Exception as ex:
#         print("EXCEPTION!")
#         os.remove(f"./{foilName}.dat")
#         return 0
#
#     if len(polar['a']) < 0.25*len(alphaArray):
#         print("TOO SHORT CONVERGENCE!!")
#         return 0
#
#     foilPolar = Airfoil.createPolarDict(polar, foilName)
#     CLmax = Airfoil.getCLmax(foilPolar)
#     LDmax = Airfoil.getLDmax(foilPolar)
#     CDmin = Airfoil.getCDmin(foilPolar)
#     LDmaxLOC = Airfoil.getLDmaxLOC(foilPolar)
#     CDminLOC = Airfoil.getCDminLOC(foilPolar)
#
#     fitness = LDmax
#
#     print(f"FITNESS: {fitness}\n\n")
#
#     if not math.isnan(fitness):
#         return fitness
#     else:
#         return 0
#
# # controlPoints = [
# #     1, 0.001,         # trailing edge (top)
# #     0.76, 0.08,
# #     0.52, 0.125,
# #     0.25, 0.12,
# #     0.1, 0.08,
# #     0, 0.03,          # leading edge (top)
# #     0, -0.03,         # leading edge (bottom)
# #     0.15, -0.08,
# #     0.37, -0.01,
# #     0.69, 0.04,
# #     1, -0.001         # trailing edge (bottom)
# # ]
#
# gene_space = [
#     [1], {'low': 0, 'high': 0.01},                              # Trailing Edge (TOP)
#
#     {'low': 0.76, 'high': 1}, {'low': 0.05, 'high': 0.2},
#     {'low': 0.52, 'high': 0.76}, {'low': 0.05, 'high': 0.2},
#     {'low': 0.25, 'high': 0.52}, {'low': 0.05, 'high': 0.2},
#     {'low': 0.1, 'high': 0.25}, {'low': 0.05, 'high': 0.2},
#
#     [0], {'low': 0.01, 'high': 0.1},                            # Leading Edge (TOP)
#     [0], {'low': -0.1, 'high': -0.01},                          # Leading Edge (BOTTOM)
#
#     {'low': 0.15, 'high': 0.37}, {'low': -0.2, 'high': -0.05},
#     {'low': 0.37, 'high': 0.69}, {'low': -0.2, 'high': -0.05},
#     {'low': 0.69, 'high': 1}, {'low': -0.2, 'high': -0.05},
#
#     [1], {'low': -0.01, 'high': 0},                             # Trailing Edge (BOTTOM)
# ]
#
# num_generations = 50
# num_parents_mating = 4
# num_genes = 22
# parent_selection_type = "sss"
# keep_parents = 2
# crossover_type = "single_point"
# mutation_type = "random"
# mutation_percent_genes = 10
#
# ga_instance = pygad.GA(num_generations=num_generations,
#                            num_parents_mating=num_parents_mating,
#                            fitness_func=fitnessFunction,
#                            num_genes=num_genes,
#                            sol_per_pop=20,
#                            parent_selection_type=parent_selection_type,
#                            keep_parents=keep_parents,
#                            crossover_type=crossover_type,
#                            mutation_type=mutation_type,
#                            mutation_percent_genes=mutation_percent_genes,
#                            gene_space=gene_space,
#                            save_solutions=True)
#
# ga_instance.run()
# ga_instance.save("Bezier Test")
# ga_instance.plot_fitness()
# solution, solution_fitness, solution_idx = ga_instance.best_solution()
# print("Parameters of the best solution : {solution}".format(solution=solution))
# print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
# print("Index of the best solution : {solution_idx}".format(solution_idx=solution_idx))
# GATools.animateGA('Bezier Test', 'bezierLDmax', 'BEZIER')
