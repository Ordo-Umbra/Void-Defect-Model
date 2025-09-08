import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh

# Parameters from paper
E_i = 1.0  # Defect energy
R_i = 2.0  # Scale
V0 = 10.0  # Adjust to ~14 for deeper well if needed (matches your plot ~V0=10)
sigma = 2.0
c = 1.0  # Emergent speed
delta_t = 1.0  # Tick step (Planck-like)
rho0 = 1.0  # For dispersion
phi_crit = 0.5 * c**2  # Horizon crit (fold=1)

# Grid
size = 100
x = np.linspace(-10, 10, size)
y = np.linspace(-10, 10, size)
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2)

# Φ for single defect
def phi_single(frame):
    strength = min(frame / 10.0, 1.0)
    return strength * E_i * np.exp(-R**2 / (2 * R_i**2))

# Gradient
def grad_phi(phi):
    dy, dx = np.gradient(phi)
    return -dx, -dy  # Attractive

# Winding: second defect (persistent structure)
r2 = np.array([5.0, 0.0])  # Init pos
v2 = np.array([0.0, 0.5])  # Init vel for orbit
def update_winding(phi):
    global r2, v2
    # Eval ∇Φ at r2 (approx central + self)
    dist = np.linalg.norm(r2)
    if dist > 0:
        grad_mag = E_i / (R_i**2) * np.exp(-dist**2 / (2 * R_i**2))
        grad = (r2 / dist) * grad_mag
        v2 += delta_t * -grad  # Tick update (Ch2.2)
        r2 += delta_t * v2

# Emergent wave (dispersion ω ≈ c k for small k)
def wave(frame, k=0.5):
    omega = np.sqrt(rho0 * k**2)  # Simplified ˆK(k) ≈1 for small k
    return np.sin(2 * np.pi * k * (R - omega * frame / 5.0)) / (R + 1e-6)

# Bound solver (corrected finite diff for -d²/dr² + V)
def solve_bound():
    N = 1000
    r_max = 10
    dr = r_max / N
    r = np.linspace(dr/2, r_max - dr/2, N)
    V = -V0 * np.exp(-r**2 / sigma**2)
    lower = (1/dr**2) * np.ones(N-1)
    main = -2/dr**2 * np.ones(N) + V
    upper = (1/dr**2) * np.ones(N-1)
    H = diags([lower, main, upper], [-1, 0, 1], shape=(N, N), format='csr')
    eigenvalues, eigenvectors = eigsh(H, k=5, which='LM', sigma=-V0-1)
    return r, eigenvalues, eigenvectors.T

# Static bound plot
r_bound, En, psi = solve_bound()
fig_bound, ax_bound = plt.subplots(figsize=(8, 6))
ax_bound.plot(r_bound, -V0 * np.exp(-r_bound**2 / sigma**2), 'k--', label='V(r)')
scale = 0.5 / np.max(np.abs(psi), axis=1)[:, np.newaxis]  # Normalize waves
for i, e in enumerate(En):
    ax_bound.plot(r_bound, scale[i] * psi[i] + e, label=f'En[{i}] ≈ {e:.2f}')
ax_bound.set_title('Discrete Mass Spectra (Bound States, Ch2.7)')
ax_bound.set_xlabel('r')
ax_bound.set_ylabel('Energy / ψ (scaled)')
ax_bound.legend()
plt.savefig('../assets/figures/bound_states.png')
plt.close(fig_bound)

# Animation
fig, ax = plt.subplots(figsize=(6, 6))
im = ax.imshow(phi_single(0), cmap='plasma', extent=[-10, 10, -10, 10])
quiver = ax.quiver(X[::5, ::5], Y[::5, ::5], *grad_phi(phi_single(0))[::5, ::5], color='white')
contour = ax.contour(X, Y, phi_single(0), levels=[phi_crit], colors='red', linestyles='--')
title = ax.set_title('Step 1: Uniform Void Field')

def update(frame):
    if frame < 10:
        field = phi_single(frame)
        step = 'Step 1: Uniform Void Field'
    elif frame < 20:
        field = phi_single(10)
        step = 'Step 2: Defect Introduction (Φ Field)'
    elif frame < 50:
        update_winding(field)  # Tick-based winding
        dist2 = np.sqrt((X - r2[0])**2 + (Y - r2[1])**2)
        field2 = E_i * np.exp(-dist2**2 / (2 * R_i**2))
        field = phi_single(10) + field2  # Superposition (Ch2.1)
        step = 'Step 3: Recursive Windings (Particle Formation)'
    else:
        field = phi_single(10) + wave(frame - 50)
        step = 'Step 4: Field Generation & Emergent Waves (Ch2.4)'
    
    grad_x, grad_y = grad_phi(field)
    im.set_array(field)
    quiver.set_UVC(grad_x[::5, ::5], grad_y[::5, ::5])
    for coll in contour.collections:
        coll.remove()
    ax.contour(X, Y, field, levels=[phi_crit], colors='red', linestyles='--')  # Horizon (Ch2.5)
    title.set_text(step)
    return [im, quiver]

ani = FuncAnimation(fig, update, frames=70, interval=100, blit=False)
ani.save('../assets/figures/particle_aspects.gif', writer=PillowWriter(fps=10))
plt.close(fig)
