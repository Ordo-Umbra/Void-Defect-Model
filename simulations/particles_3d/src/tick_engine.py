import numpy as np
from physics import compute_force

def initialize_particles(n):
    positions = np.random.uniform(-1, 1, (n, 3))
    velocities = np.zeros((n, 3))
    energies = np.ones(n) * 1.0
    ranges = np.ones(n) * 0.5
    return positions, velocities, energies, ranges

def tick(positions, velocities, energies, ranges, dt=0.01):
    new_positions = positions.copy()
    new_velocities = velocities.copy()
    for i in range(len(positions)):
        force = compute_force(i, positions, energies, ranges)
        new_velocities[i] += dt * force
        new_positions[i] += dt * new_velocities[i]
    return new_positions, new_velocities

def run_simulation(n_particles=10, n_ticks=100, dt=0.01):
    positions, velocities, energies, ranges = initialize_particles(n_particles)
    trajectory = [positions.copy()]
    for _ in range(n_ticks):
        positions, velocities = tick(positions, velocities, energies, ranges, dt)
        trajectory.append(positions.copy())
    return trajectory
