import os
import joblib

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)


# ==========================================
# LOAD BREAST CANCER DATASET
# ==========================================

data = load_breast_cancer()

X = data.data
y = data.target


print("Dataset loaded successfully")
print("Number of samples:", X.shape[0])
print("Number of features:", X.shape[1])

print("\nTarget classes:")
print(data.target_names)


# ==========================================
# TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ==========================================
# CREATE RANDOM FOREST MODEL
# ==========================================

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced"
)


# ==========================================
# TRAIN MODEL
# ==========================================

print("\nTraining model...")

model.fit(
    X_train,
    y_train
)

print("Training completed.")


# ==========================================
# PREDICTION
# ==========================================

y_pred = model.predict(X_test)

y_probability = model.predict_proba(X_test)


# ==========================================
# MODEL ACCURACY
# ==========================================

accuracy = accuracy_score(
    y_test,
    y_pred
)


# ==========================================
# ROC-AUC
# ==========================================

# Class 0 = malignant
malignant_probability = y_probability[:, 0]

roc_auc = roc_auc_score(
    y_test,
    malignant_probability
)


# ==========================================
# RESULTS
# ==========================================

print("\n==========================================")
print("BREAST CANCER MODEL RESULTS")
print("==========================================")

print(
    f"\nAccuracy: {accuracy * 100:.2f}%"
)

print(
    f"ROC-AUC: {roc_auc:.4f}"
)


print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=data.target_names
    )
)


print("\nConfusion Matrix:")

print(
    confusion_matrix(
        y_test,
        y_pred
    )
)


# ==========================================
# SAVE MODEL
# ==========================================

model_path = os.path.join(
    os.path.dirname(__file__),
    "breast_cancer_model.pkl"
)



joblib.dump(
    model,
    model_path
)


print("\n==========================================")
print("MODEL SAVED SUCCESSFULLY")
print("==========================================")

print(model_path)
