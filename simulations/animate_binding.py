import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import imageio  # For GIF save

# Use same params as binding sim
N_def = 3
positions = np.random.uniform(-1.0, 1.0, (N_def, 2))
velocities = np.random.uniform(-0.1, 0.1, (N_def, 2))
E = np.ones(N_def) * 1.0
R = np.ones(N_def) * 2.0
dt = 0.01
n_steps = 1000  # Shorter for quick anim

# Evolve and store traj
traj = np.zeros((n_steps, N_def, 2))
traj[0] = positions
for t in range(1, n_steps):
    forces = np.zeros((N_def, 2))
    for i in range(N_def):
        for j in range(N_def):
            if i == j: continue
            dr = positions[i] - positions[j]
            d = np.linalg.norm(dr)
            if d < 1e-6: continue
            K = np.exp(-d**2 / (2 * R[j]**2))
            forces[i] += -E[j] * (1 / R[j]**2) * K * dr
    velocities += dt * forces
    positions += dt * velocities
    traj[t] = positions

# Animation
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
lines = [ax.plot([], [], label=f'Defect {i+1}')[0] for i in range(N_def)]
ax.legend()

def update(frame):
    for i, line in enumerate(lines):
        line.set_data(traj[:frame, i, 0], traj[:frame, i, 1])
    return lines

anim = FuncAnimation(fig, update, frames=n_steps, interval=20, blit=True)
anim.save('assets/figures/particle_binding.gif', writer='imagemagick', fps=30)
plt.close()  # No show, just save 
