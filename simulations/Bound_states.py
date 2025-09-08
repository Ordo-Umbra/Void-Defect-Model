import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh
import matplotlib.pyplot as plt

# Parameters (tunable to match chapter examples)
V0 = 10.0  # Potential depth
sigma = 2.0  # Scale
N = 2000  # Grid points for accuracy
L = 20.0  # Domain [-L, L]
dr = 2 * L / (N - 1)
r = np.linspace(-L, L, N)

# Gaussian potential V(r) = -V0 exp(-r² / σ²)
V = -V0 * np.exp(-r**2 / sigma**2)

# Finite difference for d²/dr²
data = [np.ones(N-1)/dr**2, -2*np.ones(N)/dr**2, np.ones(N-1)/dr**2]
offsets = [-1, 0, 1]
D2 = diags(data, offsets)

# Hamiltonian H = -D2 + diag(V)
V_diag = diags(V, 0)
H = -D2 + V_diag

# Compute 5 most negative eigenvalues/vectors (bound states)
evals, evecs = eigsh(H, k=5, which='SA')

# Plot potential and wavefunctions (scaled for visibility)
plt.figure(figsize=(10, 6))
plt.plot(r, V, 'k-', label='V(r)', linewidth=2)

scale = 2.0  # Adjust to fit wavefunctions nicely
for i in range(len(evals)):
    if evals[i] >= 0: continue  # Only bound states
    psi = evecs[:, i]
    psi /= np.max(np.abs(psi))  # Normalize
    plt.plot(r, evals[i] + scale * psi**2, label=f'E_{i} ≈ {evals[i]:.2f}')

plt.xlabel('r')
plt.ylabel('Energy / |ψ(r)|²')
plt.title('Emergent Particle Levels from Defect Potential')
plt.xlim([-5 * sigma, 5 * sigma])
plt.ylim([min(V) - 1, 2])
plt.legend()
plt.grid(True)
plt.savefig('assets/figures/bound_states.png')
plt.show()  # Optional: Display during run
