import numpy as np
from physics import compute_field

def sample_field(positions, energies, ranges, grid_size=20, bounds=((-1,1),(-1,1),(-1,1))):
    x_min, x_max = bounds[0]
    y_min, y_max = bounds[1]
    z_min, z_max = bounds[2]

    x = np.linspace(x_min, x_max, grid_size)
    y = np.linspace(y_min, y_max, grid_size)
    z = np.linspace(z_min, z_max, grid_size)

    field_grid = np.zeros((grid_size, grid_size, grid_size))

    for i, xi in enumerate(x):
        for j, yj in enumerate(y):
            for k, zk in enumerate(z):
                point = np.array([xi, yj, zk])
                field_grid[i, j, k] = compute_field(point, positions, energies, ranges)

    return field_grid, x, y, z
