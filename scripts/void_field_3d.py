# scripts/void_field_3d.py

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D

# ── Setup output directory ─────────────────────────────────────────────
os.makedirs('assets/animations', exist_ok=True)

# ── Simulation parameters ─────────────────────────────────────────────
grid_size   = 100
num_defects = 5
frames      = 60
dt          = 0.05

# ── Create grid ─────────────────────────────────────────────────────────
x = np.linspace(-5, 5, grid_size)
y = np.linspace(-5, 5, grid_size)
X, Y = np.meshgrid(x, y)

# ── Initialize defects ─────────────────────────────────────────────────
np.random.seed(123)
positions  = np.random.uniform(-4, 4, (num_defects, 2))
energies   = np.random.uniform(5, 15, num_defects)
scales     = np.random.uniform(0.5, 1.5, num_defects)
velocities = np.random.normal(0, 0.1, (num_defects, 2))

# ── Field & gradient helpers ──────────────────────────────────────────
def compute_field(pos, E, R):
    dx = X - pos[0]
    dy = Y - pos[1]
    dist2 = dx**2 + dy**2
    return E * np.exp(-2 * R**2 * dist2)

def compute_gradients(phi):
    grad_y, grad_x = np.gradient(phi, y, x)
    return grad_x, grad_y

# ── Setup figure & 3D axis ─────────────────────────────────────────────
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.set_zlim(0, energies.max())

# initial field
phi = sum(compute_field(positions[i], energies[i], scales[i])
          for i in range(num_defects))
surf = ax.plot_surface(X, Y, phi, cmap='viridis', linewidth=0, antialiased=False)

# ── Animation update ──────────────────────────────────────────────────
def update(frame):
    global positions, velocities, surf

    # remove previous surface safely
    global surf
    surf.remove()
    
    # compute current field & gradients
    phi = sum(compute_field(positions[i], energies[i], scales[i])
              for i in range(num_defects))
    grad_x, grad_y = compute_gradients(phi)

    # update each defect
    for i in range(num_defects):
        ix = np.clip(int((positions[i,0] - x[0]) / (x[-1]-x[0]) * (grid_size-1)), 0, grid_size-1)
        iy = np.clip(int((positions[i,1] - y[0]) / (y[-1]-y[0]) * (grid_size-1)), 0, grid_size-1)
        acc = -np.array([grad_x[iy, ix], grad_y[iy, ix]])
        velocities[i] += acc * dt
        positions[i] += velocities[i] * dt
        positions[i] = np.clip(positions[i], -5, 5)

    # draw new surface
    surf = ax.plot_surface(X, Y, phi, cmap='viridis', linewidth=0, antialiased=False)

    # rotate the view
    ax.view_init(elev=30, azim=frame * 360/frames)
    return surf,

ani = animation.FuncAnimation(fig,
                              update,
                              frames=frames,
                              interval=100,
                              blit=False)

# ── Save animation ─────────────────────────────────────────────────────
ani.save('assets/animations/void_field_3d.mp4',
         writer='ffmpeg',
         dpi=100,
         fps=15)

plt.close(fig)
print("3D animation saved ▶ assets/animations/void_field_3d.mp4")
