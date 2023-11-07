import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import splprep, splev

def load_airfoil_data(file_path):
    return np.loadtxt(file_path, skiprows=1)

def separate_surfaces(airfoil_data):
    leading_edge_index = np.argmin(airfoil_data[:, 0])
    upper_surface_data = airfoil_data[:leading_edge_index+1][::-1]
    lower_surface_data = airfoil_data[leading_edge_index:]
    return upper_surface_data, lower_surface_data

def chebyshev_nodes(num_control_points):
    i = np.arange(num_control_points)
    nodes = np.cos((2 * i + 1) * np.pi / (2 * num_control_points))
    nodes = 0.5 * (nodes + 1)  # Shift nodes to the interval [0, 1]
    return nodes

def fit_spline_and_select_control_points_chebyshev(surface_data, num_control_points):
    tck, u = splprep([surface_data[:, 0], surface_data[:, 1]], s=0, k=3)
    chebyshev_u = chebyshev_nodes(num_control_points)
    chebyshev_points = splev(chebyshev_u, tck)
    return np.column_stack(chebyshev_points), tck

# Set these variables directly in your code or as part of a function call.
dat_file_path = '../clarky.dat'  # Replace with your actual .dat file path
num_control_points = 20  # Adjust as needed for your specific case

# Load airfoil data from the specified file
airfoil_data = load_airfoil_data(dat_file_path)

# Separate the airfoil data into upper and lower surfaces
upper_surface_data, lower_surface_data = separate_surfaces(airfoil_data)

# Fit cubic splines to the upper and lower surfaces using Chebyshev nodes
control_points_upper_cheb, tck_upper_cheb = fit_spline_and_select_control_points_chebyshev(upper_surface_data, num_control_points)
control_points_lower_cheb, tck_lower_cheb = fit_spline_and_select_control_points_chebyshev(lower_surface_data, num_control_points)

# Plot the airfoil data and control points
plt.figure(figsize=(12, 6))
plt.plot(airfoil_data[:, 0], airfoil_data[:, 1], 'k.-', label='ClarkY')
plt.plot(control_points_upper_cheb[:, 0], control_points_upper_cheb[:, 1], 'ro', label='Upper Control Points (Chebyshev)')
plt.plot(control_points_lower_cheb[:, 0], control_points_lower_cheb[:, 1], 'bo', label='Lower Control Points (Chebyshev)')

# Generate a dense set of points for spline evaluation
u_dense = np.linspace(0, 1, 1000)
x_dense, y_dense_upper = splev(u_dense, tck_upper_cheb)
_, y_dense_lower = splev(u_dense, tck_lower_cheb)
plt.plot(x_dense, y_dense_upper, 'r--', label='Upper Surface Spline (Chebyshev)')
plt.plot(x_dense, y_dense_lower, 'b--', label='Lower Surface Spline (Chebyshev)')

plt.legend()
plt.title('Airfoil with Chebyshev Node Fitted Cubic Spline Control Points')
plt.xlabel('Chord Length')
plt.ylabel('Profile Height')
plt.axis('equal')
plt.grid(True)
plt.show()
