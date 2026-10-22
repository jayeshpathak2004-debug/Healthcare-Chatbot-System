from datasets import load_dataset
import pandas as pd

print("Downloading symptom-to-diagnosis dataset...")

dataset = load_dataset("gretelai/symptom_to_diagnosis")

print("\nDataset downloaded successfully!")
print(dataset)

for split in dataset:
    df = dataset[split].to_pandas()

    print("\n" + "=" * 60)
    print("Split:", split)
    print("Records:", len(df))
    print("Columns:", df.columns.tolist())

    print("\nFirst 10 records:")
    print(df.head(10).to_string(index=False))

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDiagnosis counts:")
    print(df["output_text"].value_counts())

    print("\nNumber of unique diagnoses:")
    print(df["output_text"].nunique())

print("\nDataset inspection completed!")