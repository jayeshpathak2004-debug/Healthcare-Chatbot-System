"""
unsupervised_module.py
------------------------
UNSUPERVISED LEARNING component of the Disease Prediction System.

Where supervised_module.py predicts a disease LABEL, this module finds
structure in patient data WITHOUT labels — useful for:

  1. K-Means Clustering       -> groups patients into risk segments
                                  (e.g. Low / Moderate / High risk) purely
                                  from their clinical measurements.
  2. PCA (Dimensionality      -> compresses many clinical features into 2
     Reduction)                  components for visualization and to feed
                                  faster downstream models.
  3. Isolation Forest         -> flags anomalous / outlier patient records
     (Anomaly Detection)         (e.g. data-entry errors or rare extreme
                                  cases a clinician should double check).
  4. Hierarchical Clustering  -> agglomerative clustering + dendrogram,
                                  useful in the report to justify the
                                  chosen number of risk clusters.

Outputs (cluster plots, silhouette scores, anomaly flags) are saved to
/outputs so they can be dropped straight into the project report.
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.ensemble import IsolationForest
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import dendrogram, linkage

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
DATA_DIR = os.path.join(BASE_DIR, "data")
OUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

RANDOM_STATE = 42


def run_unsupervised_analysis(csv_path, target_col, disease_name, k_range=(2, 3, 4, 5)):
    df = pd.read_csv(csv_path)
    X = df.drop(columns=[target_col])  # unsupervised = no labels used for fitting

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # ---- 1. Choose K via silhouette score, then fit K-Means ----
    sil_scores = {}
    for k in k_range:
        km = KMeans(n_clusters=k, n_init=10, random_state=RANDOM_STATE)
        labels = km.fit_predict(X_scaled)
        sil_scores[k] = silhouette_score(X_scaled, labels)

    best_k = max(sil_scores, key=sil_scores.get)
    kmeans = KMeans(n_clusters=best_k, n_init=10, random_state=RANDOM_STATE)
    cluster_labels = kmeans.fit_predict(X_scaled)

    # Rank clusters into Low/Moderate/High risk using the *actual* label
    # rate within each cluster purely for reporting/validation purposes
    # (not used during clustering itself).
    df_report = X.copy()
    df_report["Cluster"] = cluster_labels
    df_report["ActualLabel"] = df[target_col].values
    risk_by_cluster = df_report.groupby("Cluster")["ActualLabel"].mean().sort_values()
    risk_order = {c: i for i, c in enumerate(risk_by_cluster.index)}
    risk_names = ["Low Risk", "Moderate Risk", "High Risk", "Very High Risk", "Extreme Risk"]
    df_report["RiskSegment"] = df_report["Cluster"].map(
        lambda c: risk_names[risk_order[c]] if risk_order[c] < len(risk_names) else f"Segment {c}"
    )

    # ---- 2. PCA for 2D visualization ----
    pca = PCA(n_components=2, random_state=RANDOM_STATE)
    components = pca.fit_transform(X_scaled)

    plt.figure(figsize=(7, 5))
    scatter = plt.scatter(components[:, 0], components[:, 1], c=cluster_labels, cmap="viridis", s=15, alpha=0.7)
    plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% variance)")
    plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% variance)")
    plt.title(f"{disease_name.title()} — Patient Risk Clusters (PCA-reduced, k={best_k})")
    plt.colorbar(scatter, label="Cluster")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, f"{disease_name}_pca_clusters.png"), dpi=150)
    plt.close()

    # ---- 3. Hierarchical clustering dendrogram (sampled for readability) ----
    sample_idx = np.random.RandomState(RANDOM_STATE).choice(len(X_scaled), size=min(60, len(X_scaled)), replace=False)
    Z = linkage(X_scaled[sample_idx], method="ward")
    plt.figure(figsize=(10, 5))
    dendrogram(Z)
    plt.title(f"{disease_name.title()} — Hierarchical Clustering Dendrogram (sample)")
    plt.xlabel("Patient index (sample)")
    plt.ylabel("Distance")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, f"{disease_name}_dendrogram.png"), dpi=150)
    plt.close()

    # ---- 4. Isolation Forest anomaly detection ----
    iso = IsolationForest(contamination=0.03, random_state=RANDOM_STATE)
    anomaly_flags = iso.fit_predict(X_scaled)  # -1 = anomaly, 1 = normal
    n_anomalies = int((anomaly_flags == -1).sum())

    df_report["AnomalyFlag"] = np.where(anomaly_flags == -1, "Anomalous", "Normal")
    df_report.to_csv(os.path.join(OUT_DIR, f"{disease_name}_unsupervised_report.csv"), index=False)

    summary = {
        "disease": disease_name,
        "best_k": best_k,
        "silhouette_scores_by_k": {str(k): round(v, 4) for k, v in sil_scores.items()},
        "risk_segment_counts": df_report["RiskSegment"].value_counts().to_dict(),
        "anomalies_detected": n_anomalies,
        "pca_explained_variance": [round(v, 4) for v in pca.explained_variance_ratio_],
    }

    print(f"\n=== {disease_name.upper()} — Unsupervised Analysis ===")
    print(f"Best number of clusters (by silhouette score): {best_k}")
    print("Silhouette scores per k:", summary["silhouette_scores_by_k"])
    print("Risk segment sizes:", summary["risk_segment_counts"])
    print(f"Anomalous records flagged: {n_anomalies} / {len(df)}")

    return summary


if __name__ == "__main__":
    run_unsupervised_analysis(os.path.join(DATA_DIR, "diabetes.csv"), "Outcome", "diabetes")
    run_unsupervised_analysis(os.path.join(DATA_DIR, "heart.csv"), "target", "heart")
