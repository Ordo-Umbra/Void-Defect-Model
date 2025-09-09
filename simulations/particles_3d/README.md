# Particle Field Simulation – Void Defect Model

This module simulates 3D particles interacting via recursive curvature fields.  
Each particle emits a finite-range Gaussian field, and evolves based on the gradient of the total field.

## Files
- `physics.py`: Defines field kernel and force equations
- `tick_engine.py`: Runs the simulation loop
- `field_sampler.py`: Samples field values on a grid for visualization

## Usage
Run each module in Colab or a local Python environment.  
Visualizations can be added later using PyVista or matplotlib.

## License
Creative Commons Attribution-ShareAlike 4.0
