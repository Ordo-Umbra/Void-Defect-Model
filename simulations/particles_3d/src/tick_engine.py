import numpy as np
from simulation.physics import compute_force

def initialize_particles(n):
    positions = np.random.uniform(-2, 2, (n, 3))
    velocities = np.random.uniform(-0.2, 0.2, (n, 3))
    energies = np.random.uniform(1.0, 5.0, n)
    ranges = np.random.uniform(0.5, 1.5, n)
    return positions, velocities, energies, ranges

def tick(positions, velocities, energies, ranges, dt=0.01, chaos_amp=0.05):
    new_pos = positions.copy()
    new_vel = velocities.copy()
    for i in range(len(positions)):
        force = compute_force(i, positions, energies, ranges)
        chaos = np.random.uniform(-1, 1, 3) * chaos_amp
        new_vel[i] += dt * force + chaos
        new_pos[i] += dt * new_vel[i]
    return new_pos, new_vel

def run_simulation(n_particles=100, n_ticks=500, dt=0.01, chaos_amp=0.05):
    positions, velocities, energies, ranges = initialize_particles(n_particles)
    trajectory = [positions.copy()]
    for _ in range(n_ticks):
        positions, velocities = tick(positions, velocities, energies, ranges, dt, chaos_amp)
        trajectory.append(positions.copy())
    return trajectory, energies, ranges
