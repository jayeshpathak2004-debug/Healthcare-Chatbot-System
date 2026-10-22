from datasets import load_dataset

print("Downloading dataset...")

dataset = load_dataset("notlath/eng_dataset")

print("Dataset downloaded successfully!")
print(dataset)

print("First record:")
print(dataset["train"][0])