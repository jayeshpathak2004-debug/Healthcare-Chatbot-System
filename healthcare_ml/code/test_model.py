import joblib

# ============================================================
# LOAD TRAINED MODEL
# ============================================================

model = joblib.load("model/disease_model.pkl")


print("=" * 60)
print("       HEALTHCARE DISEASE PREDICTION SYSTEM")
print("=" * 60)

print("\nModel loaded successfully!")
print("Enter symptoms below.")
print("Type 'exit' to stop.")


# ============================================================
# PREDICTION LOOP
# ============================================================

while True:

    symptoms = input("\nEnter patient's symptoms: ")

    if symptoms.lower().strip() == "exit":
        print("\nExiting...")
        break

    if not symptoms.strip():
        print("Please enter some symptoms.")
        continue

    # --------------------------------------------------------
    # Predict disease
    # --------------------------------------------------------

    prediction = model.predict([symptoms])[0]

    # --------------------------------------------------------
    # Get prediction probabilities
    # --------------------------------------------------------

    probabilities = model.predict_proba([symptoms])[0]

    classes = model.classes_

    # --------------------------------------------------------
    # Sort probabilities
    # --------------------------------------------------------

    results = sorted(
        zip(classes, probabilities),
        key=lambda x: x[1],
        reverse=True
    )

    # --------------------------------------------------------
    # Display primary prediction
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("PREDICTION RESULT")
    print("=" * 60)

    print(f"\nPredicted Disease: {prediction}")

    # --------------------------------------------------------
    # Display top 3 predictions
    # --------------------------------------------------------

    print("\nTop 3 Possible Diseases:")

    for i, (disease, probability) in enumerate(results[:3], start=1):

        print(
            f"{i}. {disease} "
            f"({probability * 100:.2f}%)"
        )

    print("=" * 60)