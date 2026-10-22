import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report

# Load dataset
df = pd.read_csv("data/multi_disease_dataset.csv")

df = df.dropna(subset=["text", "disease"])
df = df.drop_duplicates()

X = df["text"]
y = df["disease"]

# Same split used during training
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Load trained model
model = joblib.load("model/disease_model.pkl")

# Predict
predictions = model.predict(X_test)

# Confusion matrix
cm = confusion_matrix(
    y_test,
    predictions,
    labels=model.classes_
)

print("\nDisease order:")
print(list(model.classes_))

print("\nConfusion Matrix:")
print(cm)

print("\nClassification Report:")
print(classification_report(y_test, predictions))