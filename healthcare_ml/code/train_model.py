from datasets import load_dataset
import pandas as pd
import joblib
import os

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# ============================================================
# 1. LOAD DATASET
# ============================================================

print("=" * 70)
print("HEALTHCARE DISEASE PREDICTION MODEL")
print("=" * 70)

print("\nLoading dataset...")

dataset = load_dataset("gretelai/symptom_to_diagnosis")

train_df = dataset["train"].to_pandas()
test_df = dataset["test"].to_pandas()

print("Training records:", len(train_df))
print("Testing records :", len(test_df))


# ============================================================
# 2. CLEAN DATA
# ============================================================

train_df = train_df.dropna(subset=["input_text", "output_text"])
test_df = test_df.dropna(subset=["input_text", "output_text"])

train_df = train_df.drop_duplicates()
test_df = test_df.drop_duplicates()

print("\nAfter cleaning:")
print("Training records:", len(train_df))
print("Testing records :", len(test_df))


# ============================================================
# 3. INPUT AND TARGET
# ============================================================

X_train = train_df["input_text"].astype(str)
y_train = train_df["output_text"].astype(str)

X_test = test_df["input_text"].astype(str)
y_test = test_df["output_text"].astype(str)

print("\nNumber of diseases:", y_train.nunique())

print("\nDiseases:")

for disease in sorted(y_train.unique()):
    print("-", disease)


# ============================================================
# 4. CREATE ML PIPELINE
# ============================================================

model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
            max_features=10000,
            sublinear_tf=True
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=2000,
            class_weight="balanced"
        )
    )
])


# ============================================================
# 5. TRAIN MODEL
# ============================================================

print("\nTraining model...")

model.fit(X_train, y_train)

print("Training completed!")


# ============================================================
# 6. TEST MODEL
# ============================================================

print("\nTesting model...")

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\n" + "=" * 70)
print("MODEL ACCURACY")
print("=" * 70)

print(f"\nAccuracy: {accuracy * 100:.2f}%")


# ============================================================
# 7. CLASSIFICATION REPORT
# ============================================================

print("\nClassification Report:")
print(classification_report(y_test, predictions))


# ============================================================
# 8. SAVE MODEL
# ============================================================

os.makedirs("model", exist_ok=True)

model_path = "model/disease_model.pkl"

joblib.dump(model, model_path)

print("\n" + "=" * 70)
print("MODEL SAVED")
print("=" * 70)

print(f"\nModel location: {model_path}")

print("\nTraining completed successfully!")