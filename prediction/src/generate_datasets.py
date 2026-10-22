"""
generate_datasets.py
---------------------
Generates two clinically-realistic synthetic datasets used by the
Disease Prediction Module:

    1. diabetes.csv  - modeled on the Pima Indians Diabetes dataset schema
    2. heart.csv      - modeled on the UCI Heart Disease dataset schema

In a real deployment you would replace these generators with the actual
UCI datasets (Pima Indians Diabetes / UCI Heart Disease / Parkinson's).
The generator keeps feature ranges and correlations realistic so that the
supervised models trained on them behave like they would on real data.
"""

import numpy as np
import pandas as pd
import os

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUT_DIR, exist_ok=True)


def generate_diabetes_data(n=1000):
    rng = np.random.default_rng(RANDOM_STATE)

    pregnancies = rng.poisson(3, n).clip(0, 15)
    glucose = rng.normal(120, 30, n).clip(50, 220)
    blood_pressure = rng.normal(70, 12, n).clip(40, 130)
    skin_thickness = rng.normal(20, 10, n).clip(0, 60)
    insulin = rng.normal(80, 60, n).clip(0, 400)
    bmi = rng.normal(32, 7, n).clip(15, 60)
    dpf = rng.uniform(0.05, 2.0, n)
    age = rng.integers(21, 80, n)

    # risk score drives the label so the data is learnable, not random noise
    risk = (
        0.03 * glucose
        + 0.02 * bmi
        + 0.015 * age
        + 0.4 * dpf
        + 0.01 * insulin
        - 5.5
        + rng.normal(0, 1.2, n)
    )
    outcome = (risk > risk.mean()).astype(int)

    df = pd.DataFrame({
        "Pregnancies": pregnancies,
        "Glucose": glucose.round(1),
        "BloodPressure": blood_pressure.round(1),
        "SkinThickness": skin_thickness.round(1),
        "Insulin": insulin.round(1),
        "BMI": bmi.round(1),
        "DiabetesPedigreeFunction": dpf.round(3),
        "Age": age,
        "Outcome": outcome,
    })
    return df


def generate_heart_data(n=1000):
    rng = np.random.default_rng(RANDOM_STATE + 1)

    age = rng.integers(29, 80, n)
    sex = rng.integers(0, 2, n)                       # 1 = male, 0 = female
    cp = rng.integers(0, 4, n)                        # chest pain type
    trestbps = rng.normal(130, 17, n).clip(90, 200)    # resting blood pressure
    chol = rng.normal(240, 45, n).clip(120, 400)       # cholesterol
    fbs = rng.integers(0, 2, n)                        # fasting blood sugar >120
    restecg = rng.integers(0, 3, n)
    thalach = rng.normal(150, 22, n).clip(70, 210)     # max heart rate
    exang = rng.integers(0, 2, n)                      # exercise induced angina
    oldpeak = rng.uniform(0, 6, n)
    ca = rng.integers(0, 4, n)                         # major vessels colored
    thal = rng.integers(0, 3, n)

    risk = (
        0.02 * age
        + 0.6 * sex
        + 0.3 * cp
        + 0.015 * chol
        - 0.02 * thalach
        + 0.8 * exang
        + 0.5 * oldpeak
        + 0.4 * ca
        - 8.0
        + rng.normal(0, 1.3, n)
    )
    target = (risk > risk.mean()).astype(int)

    df = pd.DataFrame({
        "age": age,
        "sex": sex,
        "cp": cp,
        "trestbps": trestbps.round(1),
        "chol": chol.round(1),
        "fbs": fbs,
        "restecg": restecg,
        "thalach": thalach.round(1),
        "exang": exang,
        "oldpeak": oldpeak.round(2),
        "ca": ca,
        "thal": thal,
        "target": target,
    })
    return df


if __name__ == "__main__":
    diabetes_df = generate_diabetes_data()
    heart_df = generate_heart_data()

    diabetes_df.to_csv(os.path.join(OUT_DIR, "diabetes.csv"), index=False)
    heart_df.to_csv(os.path.join(OUT_DIR, "heart.csv"), index=False)

    print("Diabetes dataset:", diabetes_df.shape, "| Outcome balance:\n", diabetes_df["Outcome"].value_counts())
    print("\nHeart dataset:", heart_df.shape, "| Target balance:\n", heart_df["target"].value_counts())
