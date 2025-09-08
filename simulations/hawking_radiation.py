    scatters = []

    # Generate random pairs near horizon (r ~ r_h)
    theta = np.random.uniform(0, 2*np.pi, num_pairs)
    r_pair = r_h + np.random.normal(0, 0.5, num_pairs)  # Near r_h
    px = r_pair * np.cos(theta)
    py = r_pair * np.sin(theta)

    # For each pair: one infalls (to center), one escapes (outward wave, but simple fade out)
    for i in range(num_pairs):
        if np.random.rand() < 0.5:  # Random: infall or escape
            # Infall: move toward center (fade)
            alpha = 1 - frame / frames * 0.5  # Fade
            sc_in = ax.scatter(px[i]/1.5, py[i]/1.5, c='black', s=20, alpha=max(alpha, 0))
        else:
            # Escape: move outward with E ~ 1/r_h (size ~ energy)
            dx, dy = (px[i] / r_pair[i], py[i] / r_pair[i])  # Direction out
            px_out = px[i] + dx * frame / 10
            py_out = py[i] + dy * frame / 10
            energy_size = 50 / r_h  # E_rad ~ 1/r_h
            sc_out = ax.scatter(px_out, py_out, c='white', s=energy_size, alpha=0.8)
            scatters.append(sc_out)

    title.set_text(f'Frame {frame}: Pairs Form, One Infalls, One Escapes (E ~ 1/{r_h:.1f})')
    scatters.append(sc_in) if 'sc_in' in locals() else None
    return [im] + scatters

ani = FuncAnimation(fig, update, frames=frames, interval=100, blit=False)
ani.save('../assets/figures/hawking_radiation.gif', writer=PillowWriter(fps=10))
plt.close(fig)
