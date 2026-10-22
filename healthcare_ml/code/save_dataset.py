from datasets import load_dataset
import pandas as pd
import os

print("Loading dataset...")

dataset = load_dataset("notlath/eng_dataset")

# Combine train, validation and test
train_df = dataset["train"].to_pandas()
validation_df = dataset["validation"].to_pandas()
test_df = dataset["test"].to_pandas()

df = pd.concat(
    [train_df, validation_df, test_df],
    ignore_index=True
)

# Convert numeric labels to disease names
label_names = dataset["train"].features["label"].names

df["disease"] = df["label"].apply(
    lambda x: label_names[x]
)

# Remove numeric label
df = df.drop(columns=["label"])

# Create data folder if necessary
os.makedirs("data", exist_ok=True)

# Save CSV
output_file = "data/multi_disease_dataset.csv"

df.to_csv(
    output_file,
    index=False
)

print("\nDataset saved successfully!")
print("File:", output_file)
print("Total records:", len(df))

print("\nDisease distribution:")
print(df["disease"].value_counts())

print("\nColumns:")
print(df.columns.tolist())