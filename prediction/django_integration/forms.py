from django import forms


class DiabetesForm(forms.Form):
    Pregnancies = forms.IntegerField(min_value=0, max_value=20, label="Pregnancies")
    Glucose = forms.FloatField(min_value=0, label="Glucose Level (mg/dL)")
    BloodPressure = forms.FloatField(min_value=0, label="Blood Pressure (mm Hg)")
    SkinThickness = forms.FloatField(min_value=0, label="Skin Thickness (mm)")
    Insulin = forms.FloatField(min_value=0, label="Insulin (mu U/ml)")
    BMI = forms.FloatField(min_value=0, label="Body Mass Index")
    DiabetesPedigreeFunction = forms.FloatField(min_value=0, label="Diabetes Pedigree Function")
    Age = forms.IntegerField(min_value=1, max_value=120, label="Age")


class HeartDiseaseForm(forms.Form):
    age = forms.IntegerField(min_value=1, max_value=120, label="Age")
    sex = forms.ChoiceField(choices=[(1, "Male"), (0, "Female")], label="Sex")
    cp = forms.ChoiceField(
        choices=[(0, "Typical Angina"), (1, "Atypical Angina"), (2, "Non-anginal Pain"), (3, "Asymptomatic")],
        label="Chest Pain Type",
    )
    trestbps = forms.FloatField(label="Resting Blood Pressure (mm Hg)")
    chol = forms.FloatField(label="Serum Cholesterol (mg/dl)")
    fbs = forms.ChoiceField(choices=[(1, "Yes"), (0, "No")], label="Fasting Blood Sugar > 120 mg/dl")
    restecg = forms.ChoiceField(choices=[(0, "Normal"), (1, "ST-T Abnormality"), (2, "LV Hypertrophy")], label="Resting ECG")
    thalach = forms.FloatField(label="Max Heart Rate Achieved")
    exang = forms.ChoiceField(choices=[(1, "Yes"), (0, "No")], label="Exercise Induced Angina")
    oldpeak = forms.FloatField(label="ST Depression (Oldpeak)")
    ca = forms.ChoiceField(choices=[(0, "0"), (1, "1"), (2, "2"), (3, "3")], label="Major Vessels Colored by Fluoroscopy")
    thal = forms.ChoiceField(choices=[(0, "Normal"), (1, "Fixed Defect"), (2, "Reversible Defect")], label="Thalassemia")
