import numpy as np
import matplotlib.pyplot as plt
import imageio
import os

# Create output dir if needed
os.makedirs('assets/figures', exist_ok=True)

# Same params as binding sim
N_def = 3
positions = np.random.uniform(-1.0, 1.0, (N_def, 2))
velocities = np.random.uniform(-0.1, 0.1, (N_def, 2))
E = np.ones(N_def) * 1.0
R = np.ones(N_def) * 2.0
dt = 0.01
n_steps = 1000  # Shorter for quick anim
frame_step = 10  # Save every 10th step to reduce frames/GIF size (~100 frames)

# Evolve and store traj
traj = np.zeros((n_steps, N_def, 2))
traj[0] = positions
for t in range(1, n_steps):
    forces = np.zeros((N_def, 2))
    for i in range(N_def):
        for j in range(N_def):
            if i == j: continue
            dr = positions[i] - positions[j]
            d = np.linalg.norm(dr)
            if d < 1e-6: continue
            K = np.exp(-d**2 / (2 * R[j]**2))
            forces[i] += -E[j] * (1 / R[j]**2) * K * dr
    velocities += dt * forces
    positions += dt * velocities
    traj[t] = positions

# Generate frames
frames = []
for frame in range(0, n_steps, frame_step):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_title(f'Tick: {frame * dt:.2f}')
    for i in range(N_def):
        ax.plot(traj[:frame, i, 0], traj[:frame, i, 1], label=f'Defect {i+1}')
    ax.legend()
    # Save frame as RGB array (with int cast fix)
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    height, width = int(renderer.height), int(renderer.width)  # Cast to int
    image = np.frombuffer(renderer.buffer_rgba(), dtype='uint8').reshape(height, width, 4)
    image = image[:, :, :3]  # Drop alpha for RGB
    frames.append(image)
    plt.close(fig)

# Save as GIF with imageio
imageio.mimsave('assets/figures/particle_binding.gif', frames, fps=30)
print("GIF saved to assets/figures/particle_binding.gif")

# Optional: Display in Colab
# from IPython.display import Image
# Image('assets/figures/particle_binding.gif')
