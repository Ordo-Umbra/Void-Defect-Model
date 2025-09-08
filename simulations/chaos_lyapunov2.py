import numpy as np
import matplotlib.pyplot as plt

# Parameters (simple 2-defect for quick run)
N_def = 2
positions1 = np.array([[-0.5, 0.0], [0.5, 0.0]])
positions2 = positions1.copy() + np.random.uniform(-1e-4, 1e-4, (N_def, 2))  # Perturb
velocities1 = np.array([[0.0, 0.1], [0.0, -0.1]])
velocities2 = velocities1.copy()
E = np.ones(N_def) * 1.0
R = np.ones(N_def) * 2.0
dt = 0.01
n_steps = 2000

# Function to evolve system
def evolve(pos, vel):
    traj = np.zeros((n_steps, N_def, 2))
    traj[0] = pos
    for t in range(1, n_steps):
        forces = np.zeros((N_def, 2))
        for i in range(N_def):
            for j in range(N_def):
                if i == j: continue
                dr = pos[i] - pos[j]
                d = np.linalg.norm(dr)
                if d < 1e-6: continue
                K = np.exp(-d**2 / (2 * R[j]**2))
                forces[i] += -E[j] * (1 / R[j]**2) * K * dr  # Attractive
        vel += dt * forces
        pos += dt * vel
        traj[t] = pos
    return traj

traj1 = evolve(positions1, velocities1)
traj2 = evolve(positions2, velocities2)

# Compute separations (avg over defects)
seps = np.linalg.norm(traj1 - traj2, axis=2).mean(axis=1)
seps = seps[seps > 0]  # Avoid log0
times = np.arange(len(seps)) * dt

# Lyapunov: fit ln(sep) ~ lambda * t + c (early linear regime)
fit_range = 500  # Before saturation
lambda_est = np.polyfit(times[:fit_range], np.log(seps[:fit_range]), 1)[0]
print(f"Estimated Lyapunov exponent: {lambda_est:.2f}")

# Plot divergence
plt.figure(figsize=(8, 6))
plt.semilogy(times, seps, 'b-', label='Separation')
plt.xlabel('Time (ticks)')
plt.ylabel('Trajectory Separation (log scale)')
plt.title('Chaos in Defect System: Divergence from Perturbation')
plt.legend()
plt.grid(True)
plt.savefig('assets/figures/chaos_divergence.png')
plt.show()
