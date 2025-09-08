%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from IPython.display import Image, display

# Params from Ch3.4 (defect repulsion for inflation, then clustering without dark)
grid_size = 50
num_defects = 20  # Initial random defects
delta_t = 1.0  # Tick
G_attract = 0.1  # Attraction strength for clustering
G_repel = -0.05  # Initial repulsion for inflation (negative G)

# Initial defects (positions, velocities with outward for inflation)
positions = np.random.uniform(grid_size/4, 3*grid_size/4, (num_defects, 2))  # Central-ish start
velocities = np.random.normal(0, 0.5, (num_defects, 2))  # Small random vel for repulsion phase

# Grid for density vis
x = np.linspace(0, grid_size, grid_size)
y = np.linspace(0, grid_size, grid_size)
X, Y = np.meshgrid(x, y)

# Density field ρ from defects
def density_field():
    rho = np.zeros((grid_size, grid_size))
    for pos in positions:
        r = np.sqrt((X - pos[0])**2 + (Y - pos[1])**2)
        rho += np.exp(-r**2 / 2)  # Gaussian for density
    return rho

# Update ticks: Repel first (inflation), then attract (clustering)
def update_ticks(frame):
    global positions, velocities
    G = G_repel if frame < 10 else G_attract  # Switch after early frames
    for i in range(num_defects):
        grad = np.zeros(2)
        for j in range(num_defects):
            if i != j:
                dr = positions[j] - positions[i]
                dist = np.linalg.norm(dr) + 1e-6
                grad += G * dr / dist**3  # Inverse cube for force (adjustable)
        velocities[i] += delta_t * grad
        positions[i] += delta_t * velocities[i]
        # Periodic boundaries
        positions[i] %= grid_size

# Scale factor a(t) from avg distance (expansion)
scale_factors = []
def compute_scale():
    avg_dist = 0
    count = 0
    for i in range(num_defects):
        for j in range(i+1, num_defects):
            d = np.linalg.norm(positions[i] - positions[j])
            avg_dist += min(d, grid_size - d)  # Min for periodic
            count += 1
    return avg_dist / count if count > 0 else 1

# Animation
fig, ax = plt.subplots(figsize=(6, 6))
rho = density_field()
im = ax.imshow(rho, cmap='viridis', extent=[0, grid_size, 0, grid_size])
sc = ax.scatter(positions[:,0], positions[:,1], c='red', s=20)
title = ax.set_title('VDM Cosmology: Defect Repulsion (Inflation) to Clustering (Ch3.4)')

def update(frame):
    update_ticks(frame)  # Single tick per frame
    rho = density_field()
    im.set_array(rho)
    sc.set_offsets(positions)
    scale_factors.append(compute_scale())
    phase = 'Inflation (Repulsion)' if frame < 10 else 'Clustering (No Dark Matter)'
    title.set_text(f'Tick {frame}: {phase}')
    return [im, sc]

ani = FuncAnimation(fig, update, frames=50, interval=100, blit=True)
writer = PillowWriter(fps=10, metadata=dict(loop=0))
ani.save('cosmology_expansion.gif', writer=writer)
plt.close(fig)

# Display GIF in Colab
display(Image('cosmology_expansion.gif'))

# Static scale factor plot (accelerated expansion from self-sourcing)
t = np.arange(len(scale_factors)) * delta_t
plt.figure(figsize=(8, 6))
plt.plot(t, np.array(scale_factors) / scale_factors[0], 'b-', label='a(t) ~ exp(H t) from Void Self-Sourcing')
plt.title('Scale Factor Evolution (No Dark Energy, Ch3.4)')
plt.xlabel('Ticks')
plt.ylabel('Normalized a(t)')
plt.legend()
plt.grid(True)
plt.savefig('scale_factor.png')
plt.show()
