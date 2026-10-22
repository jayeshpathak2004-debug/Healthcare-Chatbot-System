from datasets import load_dataset

dataset = load_dataset("notlath/eng_dataset")

print("Dataset labels:")
print(dataset["train"].features["label"])

print("\nUnique labels:")
print(sorted(set(dataset["train"]["label"])))

print("\nNumber of examples for each label:")

from collections import Counter

counts = Counter(dataset["train"]["label"])

for label, count in sorted(counts.items()):
    print(label, "=", count)