import pygad
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, rc
from IPython.display import HTML, Image

import matplotlib.pyplot as plt
from PARSEC.Parsec import foilOrdinates

rc('animation', html='html5')

ga_instance = pygad.load('LDmaxOptimizedV1')

solutionsArr = ga_instance.solutions

"""ANIMATION"""
# Initial
X, Y = foilOrdinates(solutionsArr[0])
fig, ax = plt.subplots()
ax.set_xlim(( 0, 1))
ax.set_ylim(( -0.5, 0.5))
plt.gca().set_aspect('equal')
line, = ax.plot([], [], lw=2)


def init():
    line.set_data([], [])
    return (line,)


def animate(i):
    X, Y = foilOrdinates(solutionsArr[i])
    line.set_data(X, Y)
    plt.gca().set_aspect('equal')
    return (line,)


anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=len(solutionsArr), interval=20, blit=True)

f = f"./animation.gif"
writergif = animation.PillowWriter(fps=30)
anim.save(f, writer=writergif)
