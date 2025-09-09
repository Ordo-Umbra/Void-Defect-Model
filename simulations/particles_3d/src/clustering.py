import numpy as np
from sklearn.cluster import DBSCAN

def get_cluster_colors(positions, eps=0.3, min_samples=2):
    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(positions)
    labels = clustering.labels_
    unique = np.unique(labels)
    label_map = {lbl: idx for idx, lbl in enumerate(unique)}
    colors = np.array([label_map[lbl] for lbl in labels])
    return colors.astype(float) / max(1, colors.max()), labels

def track_cluster_counts(trajectory):
    counts = []
    for frame in trajectory:
        _, labels = get_cluster_colors(frame[:, :2])
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        counts.append(n_clusters)
    return counts
