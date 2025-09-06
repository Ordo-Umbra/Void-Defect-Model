# scripts/void_field_sim.py

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

# ── Simulation parameters ─────────────────────────────────────────────
grid_size   = 100            # resolution of the field
num_defects = 5              # how many defects to seed
frames      = 100            # number of animation frames
dt          = 0.1            # time-step per tick

# spatial grid
x = np.linspace(-5, 5, grid_size)
y = np.linspace(-5, 5, grid_size)
X, Y = np.meshgrid(x, y)

# random initial defect attributes
np.random.seed(42)
positions  = np.random.uniform(-4, 4, (num_defects, 2))
energies   = np.random.uniform(5, 15, num_defects)
scales     = np.random.uniform(0.5, 1.5, num_defects)
velocities = np.random.normal(0, 0.1, (num_defects, 2))

# ── Field & gradient helpers ──────────────────────────────────────────
def compute_field(pos, E, R):
    """Return a grid of φ(x,y) = E * exp(-2 R^2 * dist^2)."""
    dx = X - pos[0]
    dy = Y - pos[1]
    dist2 = dx*dx + dy*dy
    return E * np.exp(-2 * (R**2) * dist2)

def compute_gradients(phi):
    """Numeric gradient of φ wrt x and y."""
    # np.gradient returns [dφ/dy, dφ/dx]
    grad_y, grad_x = np.gradient(phi, y, x)
    return grad_x, grad_y

# ── Setup figure ───────────────────────────────────────────────────────
fig, ax = plt.subplots()
phi0 = sum(compute_field(positions[i], energies[i], scales[i])
           for i in range(num_defects))

# initial image and scatter
im = ax.imshow(phi0,
               extent=[x[0], x[-1], y[0], y[-1]],
               origin='lower',
               cmap='viridis',
               vmin=0,
               vmax=phi0.max())
pts = ax.scatter(positions[:,0],
                 positions[:,1],
                 c='red',
                 s=50)
ax.set_title('Void Field + Defects')

# ── Animation update ──────────────────────────────────────────────────
def update(frame):
    global positions, velocities

    # 1) compute field
    phi = sum(compute_field(positions[i], energies[i], scales[i])
              for i in range(num_defects))

    # 2) compute gradient
    grad_x, grad_y = compute_gradients(phi)

    # 3) update each defect
    for i in range(num_defects):
        # find nearest grid index for this defect
        ix = np.clip(int((positions[i,0] - x[0]) / (x[-1]-x[0]) * (grid_size-1)), 0, grid_size-1)
        iy = np.clip(int((positions[i,1] - y[0]) / (y[-1]-y[0]) * (grid_size-1)), 0, grid_size-1)

        # force = -∇φ ; acceleration = force * dt
        acc = -np.array([grad_x[iy, ix], grad_y[iy, ix]])
        velocities[i] += acc * dt

        # update position
        positions[i] += velocities[i] * dt

        # optional: keep within bounds
        positions[i] = np.clip(positions[i], -5, 5)

    # 4) redraw
    im.set_data(phi)
    pts.set_offsets(positions)
    return im, pts

ani = animation.FuncAnimation(fig,
                              update,
                              frames=frames,
                              interval=100,
                              blit=True)

# ── Save as MP4 (requires ffmpeg) or GIF ──────────────────────────────
# Ensure the output directory exists
os.makedirs('assets/animations', exist_ok=True)
ani.save('assets/animations/void_defect_simulation.mp4',
         writer='ffmpeg',
         dpi=150)
# ani.save('assets/animations/void_defect_simulation.gif',
#          writer='imagemagick',
#          fps=10)

plt.close(fig)
print("Animation saved ▶ assets/animations/void_defect_simulation.mp4")
