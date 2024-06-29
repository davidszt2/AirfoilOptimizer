import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import splprep, splev

def loadAirfoil(file_path):
    return np.loadtxt(file_path, skiprows=1)

def sepSurfaces(airfoil_data):
    leading_edge_index = np.argmin(airfoil_data[:, 0])
    upper_surface_data = airfoil_data[:leading_edge_index+1][::-1]
    lower_surface_data = airfoil_data[leading_edge_index:]
    return upper_surface_data, lower_surface_data

def chebyshevNodes(nPoints):
    i = np.arange(nPoints)
    nodes = np.cos((2 * i + 1) * np.pi / (2 * nPoints))
    nodes = 0.5 * (nodes + 1)  # Shift nodes to the interval [0, 1]
    return nodes

def airfoilControlPoints(airfoil, nPoints):
    airfoilData = loadAirfoil(airfoil)
    upperSurf, lowerSurf = sepSurfaces(airfoilData)

    # Upper Surface
    tckUpper, uUpper = splprep([upperSurf[:, 0], upperSurf[:, 1]], s=0, k=3)
    chebyshev_uUpper = chebyshevNodes(nPoints)
    chebyshev_pointsUpper = splev(chebyshev_uUpper, tckUpper)
    chebyshev_pointsUpperConcat = [[i, j] for i, j in zip(chebyshev_pointsUpper[0], chebyshev_pointsUpper[1])]

    # Lower Surface
    tckLower, uLower = splprep([lowerSurf[:, 0], lowerSurf[:, 1]], s=0, k=3)
    chebyshev_uLower = chebyshevNodes(nPoints)
    chebyshev_pointsLower = splev(chebyshev_uLower, tckLower)
    chebyshev_pointsLowerConcat = [[i, j] for i, j in zip(chebyshev_pointsLower[0], chebyshev_pointsLower[1])]

    return np.vstack((chebyshev_pointsUpperConcat, chebyshev_pointsLowerConcat))

def BEZIERfoil(control_points, num_points=150):
    # Split control points into upper and lower surfaces
    half = len(control_points) // 2
    upper_control_points = control_points[:half]
    lower_control_points = control_points[half:]

    # Fit a spline for the upper surface
    tck_upper, _ = splprep([upper_control_points[:, 0], upper_control_points[:, 1]], s=0, k=3)
    u_upper_fine = np.linspace(0, 1, num_points // 2)
    x_upper_fine, y_upper_fine = splev(u_upper_fine, tck_upper)

    # Fit a spline for the lower surface
    tck_lower, _ = splprep([lower_control_points[:, 0], lower_control_points[:, 1]], s=0, k=3)
    u_lower_fine = np.linspace(0, 1, num_points // 2)
    x_lower_fine, y_lower_fine = splev(u_lower_fine, tck_lower)

    # Combine the results
    x_fine = np.concatenate([x_upper_fine, x_lower_fine[::-1]])
    y_fine = np.concatenate([y_upper_fine, y_lower_fine[::-1]])

    return x_fine, y_fine


airfoil = '../clarky.dat'
nCP = 10

controlPoints = airfoilControlPoints(airfoil, nCP)
x, y = BEZIERfoil(controlPoints, 1000)
print(controlPoints)
plt.figure()
plt.plot(x, y)
plt.axis('equal')
plt.grid(True)
plt.show()
