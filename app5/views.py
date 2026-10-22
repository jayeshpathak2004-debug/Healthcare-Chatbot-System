import os
import joblib

from django.conf import settings
from django.shortcuts import render

from .models import DiseasePrediction


# ==========================================
# LOAD TRAINED ML MODEL
# ==========================================

MODEL_PATH = os.path.join(
    settings.BASE_DIR,
    "healthcare_ml",
    "model",
    "disease_model.pkl"
)

model = joblib.load(MODEL_PATH)


# ==========================================
# ML DISEASE PREDICTION
# ==========================================

def ml_disease_prediction(request):

    result = None
    top_predictions = []
    symptoms = ""

    patient_name = ""
    age = ""
    gender = ""

    saved = False

    if request.method == "POST":

        patient_name = request.POST.get(
            "patient_name",
            ""
        ).strip()

        age = request.POST.get(
            "age",
            ""
        ).strip()

        gender = request.POST.get(
            "gender",
            ""
        ).strip()

        symptoms = request.POST.get(
            "symptoms",
            ""
        ).strip()


        # ==================================
        # PREDICT ONLY IF SYMPTOMS PROVIDED
        # ==================================

        if symptoms:

            # Main prediction
            predicted_disease = model.predict(
                [symptoms]
            )[0]


            # Prediction probabilities
            probabilities = model.predict_proba(
                [symptoms]
            )[0]

            classes = model.classes_


            # Sort probabilities highest to lowest
            results = sorted(
                zip(classes, probabilities),
                key=lambda x: x[1],
                reverse=True
            )


            # ==================================
            # TOP 3 PREDICTIONS
            # ==================================

            for disease, probability in results[:3]:

                top_predictions.append({
                    "disease": disease,
                    "probability": round(
                        probability * 100,
                        2
                    )
                })


            result = predicted_disease


            # ==================================
            # SAVE PREDICTION TO DATABASE
            # ==================================

            if patient_name:

                # Find probability of predicted disease
                predicted_probability = 0

                for disease, probability in results:

                    if disease == predicted_disease:

                        predicted_probability = (
                            probability * 100
                        )

                        break


                DiseasePrediction.objects.create(

                    patient_name=patient_name,

                    age=int(age)
                    if age.isdigit()
                    else None,

                    gender=gender,

                    symptoms=symptoms,

                    predicted_disease=predicted_disease,

                    confidence=round(
                        predicted_probability,
                        2
                    )
                )

                saved = True


    # ==========================================
    # SEND DATA TO TEMPLATE
    # ==========================================

    return render(
        request,
        "app5/ml_prediction.html",
        {
            "result": result,
            "top_predictions": top_predictions,
            "symptoms": symptoms,

            "patient_name": patient_name,
            "age": age,
            "gender": gender,

            "saved": saved,
        }
    )