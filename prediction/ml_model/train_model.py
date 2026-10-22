import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


# Load dataset
df = pd.read_csv("diabetes.csv")


# Features
features = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age"
]

X = df[features]
y = df["Outcome"]


# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Create model
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)


# Train
model.fit(X_train, y_train)


# Save model
joblib.dump(model, "diabetes_model.pkl")


# Accuracy
accuracy = model.score(X_test, y_test)

print("================================")
print("Model trained successfully!")
print("Accuracy:", accuracy)
print("Saved as diabetes_model.pkl")
print("================================")