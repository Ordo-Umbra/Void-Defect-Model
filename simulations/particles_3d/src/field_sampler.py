import numpy as np
from simulation.physics import compute_field

def sample_field(positions, energies, ranges, grid_size=50, bounds=((-2,2),(-2,2),(-2,2))):
    x_min, x_max = bounds[0]
    y_min, y_max = bounds[1]
    z_min, z_max = bounds[2]

    xs = np.linspace(x_min, x_max, grid_size)
    ys = np.linspace(y_min, y_max, grid_size)
    zs = np.linspace(z_min, z_max, grid_size)

    field_grid = np.zeros((grid_size, grid_size, grid_size))
    for i, xi in enumerate(xs):
        for j, yj in enumerate(ys):
            for k, zk in enumerate(zs):
                pt = np.array([xi, yj, zk])
                field_grid[i, j, k] = compute_field(pt, positions, energies, ranges)
    return field_grid, xs, ys, zs
