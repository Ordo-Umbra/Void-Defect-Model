import numpy as np
import matplotlib.pyplot as plt

# Grid setup
x = np.linspace(-10, 10, 200)
y = np.linspace(-10, 10, 200)
X, Y = np.meshgrid(x, y)

# Avoid division by zero
R = np.sqrt(X**2 + Y**2 + 1e-6)

# Simple inverse-radius field (defect strength)
field = 1 / R  # Could adjust to exponential decay or other forms for VDM specifics

# Plot contour
plt.figure(figsize=(8, 6))
plt.contourf(X, Y, field, levels=50, cmap='plasma')
plt.colorbar(label='Field Intensity')
plt.title('2D Void Field with Central Defect')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True, linestyle='--', alpha=0.5)

# Save to file (add to assets/figures)
plt.savefig('assets/figures/defect_field.png')
plt.show()  # Displays locally
 
