import pandas as pd
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_csv("data/multi_disease_dataset.csv")

# Remove empty records
df = df.dropna(subset=["text", "disease"])

# Remove duplicate records
df = df.drop_duplicates()

# Input and target
X = df["text"]
y = df["disease"]

# Split into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Dataset prepared successfully!")
print("Total records:", len(df))
print("Training records:", len(X_train))
print("Testing records:", len(X_test))

print("\nTraining disease distribution:")
print(y_train.value_counts())

print("\nTesting disease distribution:")
print(y_test.value_counts())