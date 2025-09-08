import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh

# Parameters from paper (Ch2/Ch3)
E_i = 1.0  # Defect energy
R_i = 2.0  # Scale
V0 = 10.0  # Potential depth
sigma = 2.0  # Width
c = 1.0  # Emergent speed
delta_t = 0.1  # Tick step
rho0 = 1.0  # For wave dispersion (placeholder)

# Grid for 2D fields
size = 100
x = np.linspace(-10, 10, size)
y = np.linspace(-10, 10, size)
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2)

# Curvature field for single defect at origin
def phi_single(frame):
    strength = min(frame / 10, 1)  # Gradual intro
    return strength * E_i * np.exp(-R**2 / (2 * R_i**2))

# Gradient (force field)
def grad_phi(phi):
    dy, dx = np.gradient(phi)
    return -dx, -dy  # -∇Φ for attraction

# Add winding: second defect orbiting
r2 = np.array([5.0, 0.0])  # Initial position
v2 = np.array([0.0, 0.5])  # Initial velocity for orbit
def update_winding():
    global r2, v2
    dist = np.linalg.norm(r2)
    grad = (r2 / (dist + 1e-6)) * (E_i * r2 / R_i**2 * np.exp(-dist**2 / (2 * R_i**2)))  # Approx ∇Φ at r2
    v2 += delta_t * -grad  # Attract
    r2 += delta_t * v2

# Wave fluctuation (emergent limit)
def wave(frame):
    k = 0.5  # Wave number
    return np.sin(2 * np.pi * (R - c * frame / 5) * k) / (R + 1e-6)  # Simple dispersion analogy

# Bound state solver (1D Schrödinger-like for mass spectra)
def solve_bound():
    N = 1000
    r_max = 10
    dr = r_max / N
    r = np.linspace(dr/2, r_max - dr/2, N)
    V = -V0 * np.exp(-r**2 / sigma**2)
    diagonals = [1/dr**2 + V/2, -2/dr**2 + V, 1/dr**2 + V/2]
    H = diags(diagonals, [-1, 0, 1], shape=(N, N), format='csr')
    eigenvalues, eigenvectors = eigsh(H, k=5, which='LM', sigma=-V0)  # Find lowest (negative) En
    return r, eigenvalues, eigenvectors.T

# Plot bound states (static image)
r_bound, En, psi = solve_bound()
fig_bound, ax_bound = plt.subplots(figsize=(8, 6))
ax_bound.plot(r_bound, -V0 * np.exp(-r_bound**2 / sigma**2), 'k--', label='V(r)')
for i, e in enumerate(En):
    ax_bound.plot(r_bound, psi[i] * 5 + e, label=f'En[{i}] ≈ {e:.2f}')
ax_bound.set_title('Discrete Mass Spectra (Bound States)')
ax_bound.set_xlabel('r')
ax_bound.set_ylabel('Energy / ψ')
ax_bound.legend()
plt.savefig('../assets/figures/bound_states.png')
plt.close(fig_bound)

# Animation for steps 1-4
fig, ax = plt.subplots(figsize=(6, 6))
im = ax.imshow(phi_single(0), cmap='plasma', extent=[-10, 10, -10, 10])
quiver = ax.quiver(X[::5, ::5], Y[::5, ::5], *grad_phi(phi_single(0))[::5, ::5], color='white')
title = ax.set_title('Step 1: Uniform Void Field')

def update(frame):
    if frame < 10:
        field = phi_single(frame)
        grad_x, grad_y = grad_phi(field)
        step = 'Step 1: Uniform Void Field'
    elif frame < 20:
        field = phi_single(10)
        grad_x, grad_y = grad_phi(field)
        step = 'Step 2: Defect Introduction (Φ Field)'
    elif frame < 50:
        update_winding()  # Simulate winding
        field1 = E_i * np.exp(-np.sqrt((X - r2[0])**2 + (Y - r2[1])**2)**2 / (2 * R_i**2))
        field = phi_single(10) + field1  # Superposition
        grad_x, grad_y = grad_phi(field)
        step = 'Step 3: Recursive Windings (Particle Formation)'
    else:
        field = phi_single(10) + wave(frame - 50)
        grad_x, grad_y = grad_phi(field)
        step = 'Step 4: Field Generation (Gradients & Waves)'
    
    im.set_array(field)
    quiver.set_UVC(grad_x[::5, ::5], grad_y[::5, ::5])
    title.set_text(step)
    return [im, quiver]

ani = FuncAnimation(fig, update, frames=70, interval=100, blit=False)
ani.save('../assets/figures/particle_aspects.gif', writer=PillowWriter(fps=10))
plt.close(fig)
