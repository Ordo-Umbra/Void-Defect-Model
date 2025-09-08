import numpy as np
import matplotlib.pyplot as plt

# Parameters (tunable; 5 defects for complexity)
N_def = 5
dt = 0.01
n_steps = 5000
noise_std = 0.3  # Tune ~0.3-0.5 for lambda 0.5-0.9
avg_runs = 3  # Average over runs for stable estimate

def single_run():
    positions1 = np.random.uniform(-1.0, 1.0, (N_def, 2))
    positions2 = positions1.copy() + np.random.uniform(-1e-4, 1e-4, (N_def, 2))
    velocities1 = np.random.uniform(-0.2, 0.2, (N_def, 2))
    velocities2 = velocities1.copy()
    E = np.ones(N_def) * 1.0
    R = np.ones(N_def) * 2.0

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
                    forces[i] += -E[j] * (1 / R[j]**2) * K * dr
                forces[i] += np.random.normal(0, noise_std, 2)
            vel += dt * forces
            pos += dt * vel
            traj[t] = pos
        return traj

    traj1 = evolve(positions1, velocities1)
    traj2 = evolve(positions2, velocities2)

    seps = np.linalg.norm(traj1 - traj2, axis=2).mean(axis=1)
    seps = seps[seps > 0]
    times = np.arange(len(seps)) * dt
    return times, seps

# Average over runs
all_lambdas = []
for _ in range(avg_runs):
    times, seps = single_run()
    fit_range = min(500, len(times) - 1)
    if fit_range > 10:  # Ensure enough points
        slope, intercept = np.polyfit(times[:fit_range], np.log(seps[:fit_range]), 1)
        all_lambdas.append(slope)

lambda_est = np.mean(all_lambdas) if all_lambdas else 0.0
print(f"Average Lyapunov exponent over {avg_runs} runs: {lambda_est:.2f}")

# Plot last run for figure
plt.figure(figsize=(8, 6))
plt.semilogy(times, seps, 'b-', label='Separation')
# Overlay fit
fit_seps = np.exp(intercept + slope * times[:fit_range])
plt.semilogy(times[:fit_range], fit_seps, 'r--', label=f'Fit (λ ≈ {slope:.2f})')
plt.xlabel('Time (ticks)')
plt.ylabel('Trajectory Separation (log scale)')
plt.title('Chaos in Defect System: Divergence from Perturbation')
plt.legend()
plt.grid(True)
plt.savefig('assets/figures/chaos_divergence.png')
plt.show()
