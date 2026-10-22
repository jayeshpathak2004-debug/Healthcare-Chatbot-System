import joblib

model = joblib.load("model/disease_model.pkl")

test_cases = [
    "High fever with intense headache, pain behind the eyes, muscle aches and extreme tiredness.",
    "Watery stools many times a day with abdominal cramps and nausea.",
    "Fever with chills, cough, sore throat, runny nose and body aches.",
    "High fever followed by a skin rash, red eyes and severe tiredness.",
    "Persistent cough with chest pain, shortness of breath and fever.",
    "Prolonged fever with weakness, abdominal discomfort and loss of appetite."
]

print("EXTERNAL MODEL TEST")
print("=" * 60)

for i, symptoms in enumerate(test_cases, 1):

    prediction = model.predict([symptoms])[0]

    probabilities = model.predict_proba([symptoms])[0]

    best_probability = max(probabilities) * 100

    if best_probability >= 70:
        confidence_level = "HIGH"
    elif best_probability >= 50:
        confidence_level = "MODERATE"
    else:
        confidence_level = "LOW"

    print(f"\nTest {i}")
    print("Symptoms:", symptoms)
    print("Prediction:", prediction)
    print(f"Confidence: {best_probability:.2f}%")
    print("Model confidence level:", confidence_level)