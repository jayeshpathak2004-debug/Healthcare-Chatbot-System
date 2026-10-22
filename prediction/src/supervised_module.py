"""
supervised_module.py
---------------------
SUPERVISED LEARNING component of the Disease Prediction System.

For each disease dataset (Diabetes, Heart Disease) this module:
  1. Splits data into train/test sets
  2. Scales features
  3. Trains multiple classical ML algorithms:
        - Logistic Regression
        - Support Vector Machine (SVM)
        - K-Nearest Neighbors (KNN)
        - Decision Tree
        - Random Forest
        - Naive Bayes
        - Gradient Boosting
  4. Evaluates each with Accuracy, Precision, Recall, F1-score, ROC-AUC
  5. Picks the best model per disease and saves it (model + scaler) with joblib
     so it can be loaded instantly by the Django prediction views.

This is the "multiple libraries" / "supervised" half of the project brief.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "models")
OUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

RANDOM_STATE = 42


def get_models():
    """Multiple algorithms from scikit-learn — swap/add freely."""
    return {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "SVM (RBF Kernel)": SVC(kernel="rbf", probability=True, random_state=RANDOM_STATE),
        "KNN": KNeighborsClassifier(n_neighbors=7),
        "Decision Tree": DecisionTreeClassifier(max_depth=6, random_state=RANDOM_STATE),
        "Random Forest": RandomForestClassifier(n_estimators=200, max_depth=8, random_state=RANDOM_STATE),
        "Naive Bayes": GaussianNB(),
        "Gradient Boosting": GradientBoostingClassifier(random_state=RANDOM_STATE),
    }


def train_and_evaluate(csv_path, target_col, disease_name):
    df = pd.read_csv(csv_path)
    X = df.drop(columns=[target_col])
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    results = []
    fitted_models = {}

    for name, model in get_models().items():
        model.fit(X_train_scaled, y_train)
        preds = model.predict(X_test_scaled)
        probs = model.predict_proba(X_test_scaled)[:, 1] if hasattr(model, "predict_proba") else preds

        cv_score = cross_val_score(model, X_train_scaled, y_train, cv=5).mean()

        results.append({
            "Model": name,
            "Accuracy": round(accuracy_score(y_test, preds), 4),
            "Precision": round(precision_score(y_test, preds), 4),
            "Recall": round(recall_score(y_test, preds), 4),
            "F1-Score": round(f1_score(y_test, preds), 4),
            "ROC-AUC": round(roc_auc_score(y_test, probs), 4),
            "CV Accuracy (5-fold)": round(cv_score, 4),
        })
        fitted_models[name] = model

    results_df = pd.DataFrame(results).sort_values("F1-Score", ascending=False).reset_index(drop=True)

    best_name = results_df.iloc[0]["Model"]
    best_model = fitted_models[best_name]

    # Save the winning model + the scaler + the feature column order together
    bundle = {
        "model": best_model,
        "scaler": scaler,
        "feature_names": list(X.columns),
        "model_name": best_name,
    }
    model_path = os.path.join(MODEL_DIR, f"{disease_name}_model.pkl")
    joblib.dump(bundle, model_path)

    # Save comparison table + a detailed report for the best model
    results_df.to_csv(os.path.join(OUT_DIR, f"{disease_name}_model_comparison.csv"), index=False)

    best_preds = fitted_models[best_name].predict(X_test_scaled)
    report_text = classification_report(y_test, best_preds)
    cm = confusion_matrix(y_test, best_preds).tolist()

    with open(os.path.join(OUT_DIR, f"{disease_name}_best_model_report.txt"), "w") as f:
        f.write(f"Disease: {disease_name}\n")
        f.write(f"Best Model: {best_name}\n\n")
        f.write(report_text)
        f.write(f"\nConfusion Matrix: {cm}\n")

    print(f"\n=== {disease_name.upper()} — Model Comparison ===")
    print(results_df.to_string(index=False))
    print(f"Best model: {best_name}  -> saved to {model_path}")

    return results_df, best_name, model_path


if __name__ == "__main__":
    train_and_evaluate(os.path.join(DATA_DIR, "diabetes.csv"), "Outcome", "diabetes")
    train_and_evaluate(os.path.join(DATA_DIR, "heart.csv"), "target", "heart")
