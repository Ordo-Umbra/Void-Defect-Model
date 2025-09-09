import numpy as np

def gaussian_kernel(d, R):
    return np.exp(-2 * (R**2) * (d**2))

def compute_field(x, positions, energies, ranges):
    field = 0.0
    for i in range(len(positions)):
        d = np.linalg.norm(x - positions[i])
        field += energies[i] * gaussian_kernel(d, ranges[i])
    return field

def compute_force(i, positions, energies, ranges):
    ri = positions[i]
    force = np.zeros(3)
    for j in range(len(positions)):
        if i == j:
            continue
        rj = positions[j]
        d_vec = ri - rj
        d = np.linalg.norm(d_vec)
        if d == 0:
            continue
        grad = -4 * energies[j] * (ranges[j]**2) * d_vec \
               * np.exp(-2 * (ranges[j]**2) * (d**2))
        force += grad
    return force
