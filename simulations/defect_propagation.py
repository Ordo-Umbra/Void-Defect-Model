import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter  # For GIF save

grid_size = 50
grid = np.zeros((grid_size, grid_size))

# Central defect
grid[grid_size//2, grid_size//2] = 1

# Add some random scattered defects
grid[np.random.randint(0, grid_size, 5), np.random.randint(0, grid_size, 5)] = 1

# Add a glider pattern for sustained motion (top-left area)
glider = np.array([[0, 1, 0],
                   [0, 0, 1],
                   [1, 1, 1]])
grid[5:8, 5:8] = glider  # Place it at row 5-7, col 5-7 (adjust if needed)

def update(frame):
    global grid
    new_grid = grid.copy()
    for i in range(grid_size):
        for j in range(grid_size):
            neighbors = np.sum(grid[max(0, i-1):min(grid_size, i+2), max(0, j-1):min(grid_size, j+2)]) - grid[i, j]
            if grid[i, j] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[i, j] = 0
            else:
                if neighbors == 3:
                    new_grid[i, j] = 1
    grid = new_grid
    im.set_array(grid)
    return [im]

fig, ax = plt.subplots(figsize=(6, 6))
im = ax.imshow(grid, cmap='binary')
ani = FuncAnimation(fig, update, frames=50, interval=200, blit=True)
ani.save('../assets/figures/defect_propagation.gif', writer=PillowWriter(fps=5))
plt.close(fig)
# plt.show()
