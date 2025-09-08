import numpy as np
import matplotlib.pyplot as plt

# Parameters (tuned for visible binding)
N_def = 3  # More defects for complex particle (try 5)
positions = np.random.uniform(-1.0, 1.0, (N_def, 2))  # Random close start
velocities = np.random.uniform(-0.1, 0.1, (N_def, 2))  # Small random v
E = np.ones(N_def) * 1.0
R = np.ones(N_def) * 2.0  # Larger scale for stronger pull
dt = 0.01
n_steps = 5000  # More steps to see stabilization

# Store trajectories
traj = np.zeros((n_steps, N_def, 2))
traj[0] = positions

# Evolution loop
for t in range(1, n_steps):
    forces = np.zeros((N_def, 2))
    for i in range(N_def):
        for j in range(N_def):
            if i == j: continue
            dr = positions[i] - positions[j]
            d = np.linalg.norm(dr)
            if d < 1e-6: continue
            K = np.exp(-d**2 / (2 * R[j]**2))
            # Attractive force: - E_j * (dr / R_j^2) * K  (fixed sign)
            force_contrib = - E[j] * (1 / R[j]**2) * K * dr
            forces[i] += force_contrib
    velocities += dt * forces
    positions += dt * velocities
    traj[t] = positions

# Plot trajectories
plt.figure(figsize=(8, 6))
for i in range(N_def):
    plt.plot(traj[:, i, 0], traj[:, i, 1], label=f'Defect {i+1}')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Defect Trajectories: Emergence of Bound Particle')
plt.legend()
plt.grid(True)
plt.savefig('assets/figures/particle_trajectories.png')

# Final Φ field
x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
Phi = np.zeros_like(X)
for i in range(N_def):
    d2 = (X - positions[i, 0])**2 + (Y - positions[i, 1])**2
    Phi += E[i] * np.exp(-d2 / (2 * R[i]**2))

plt.figure(figsize=(8, 6))
plt.contourf(X, Y, Phi, levels=20, cmap='viridis')
plt.colorbar(label='Φ (Curvature Field)')
plt.plot(positions[:, 0], positions[:, 1], 'ro', markersize=10, label='Defects')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Final Field: Bound Defect Structure as Particle')
plt.legend()
plt.savefig('assets/figures/particle_field.png')
plt.show()
