import numpy as np
import matplotlib.pyplot as plt

# Parameters (λ ≈0.8 from paper)
lambda_lyap = 0.8
t = np.linspace(0, 20, 200)  # Ticks
delta0 = 0.01  # Initial small separation

# Divergence: δ(t) = δ0 exp(λ t)
delta = delta0 * np.exp(lambda_lyap * t)

# Plot trajectories
plt.figure(figsize=(8, 6))
plt.plot(t, np.sin(t), label='Trajectory 1', color='blue')  # Base path
plt.plot(t, np.sin(t) + delta, label='Perturbed Trajectory 2', color='red')
plt.title('Chaos in VDM: Trajectory Divergence (Lyapunov ≈0.8)')
plt.xlabel('Ticks (t)')
plt.ylabel('Position')
plt.legend()
plt.grid(True)
plt.savefig('../assets/figures/chaos_divergence.png')
plt.close()
