import numpy as np
import matplotlib.pyplot as plt

# Parameters (tunable; start simple with 2 defects)
N_def = 2  # Number of defects (increase for complex particles)
positions = np.array([[-2.0, 0.0], [2.0, 0.0]])  # Initial positions (2D)
velocities = np.array([[0.0, 0.1], [0.0, -0.1]])  # Initial velocities (small for orbit)
E = np.ones(N_def) * 1.0  # Energies (mass-like)
R = np.ones(N_def) * 1.0  # Scales
dt = 0.01  # Time step (tick size)
n_steps = 2000  # Simulation steps

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
            if d < 1e-6: continue  # Avoid singularity
            K = np.exp(-d**2 / (2 * R[j]**2))
            # Force contrib: E_j * (1 / R_j²) * K * dr (attractive direction)
            force_contrib = E[j] * (1 / R[j]**2) * K * dr
            forces[i] += force_contrib
    velocities += dt * forces  # Update v (assume unit mass)
    positions += dt * velocities  # Update r
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

# Plot final curvature field Φ
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
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
plt.show()  # Optional
