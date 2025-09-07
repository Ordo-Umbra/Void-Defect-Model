import numpy as np
import matplotlib.pyplot as plt

def sierpinski(n):
    """Generate points for a Sierpinski triangle at iteration n."""
    points = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3)/2]])
    for _ in range(n):
        new_points = []
        for p in points:
            new_points.append(p)
            new_points.append((p + points[0]) / 2)
            new_points.append((p + points[1]) / 2)
            new_points.append((p + points[2]) / 2)
        points = np.unique(new_points, axis=0)  # Remove duplicates
    return points

# Generate at level 5 (adjust for detail)
pts = sierpinski(5)

# Plot
plt.figure(figsize=(8, 8))
plt.scatter(pts[:, 0], pts[:, 1], s=1, color='blue')
plt.title('Recursive Geometry: Sierpinski Triangle (VDM Analogy)')
plt.axis('equal')
plt.axis('off')

# Save
plt.savefig('assets/figures/sierpinski_triangle.png')
plt.show()
