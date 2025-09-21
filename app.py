from flask import Flask, render_template, request
import pandas as pd
from difflib import get_close_matches
import re

app = Flask(__name__)

# ---- Load Dataset ----
data = pd.read_csv("symptom_disease_150.csv")
symptom_columns = list(data.columns[:-3])  # All symptom columns

# ---- Synonyms Mapping ----
keyword_map = {
    "fever": "Fever",
    "high fever": "Fever",
    "low fever": "Fever",
    "headache": "Headache",
    "head ache": "Headache",
    "cough": "Cough",
    "teeth pain": "Toothache",
    "tooth pain": "Toothache",
    "knee pain": "Knee Ache",
    "joint pain": "Knee Ache",
    "nausea": "Nausea",
    "vomiting": "Vomiting",
    "fatigue": "Fatigue",
    "cold": "Cold",
    "sore throat": "Sore Throat",
    "heart pain": "Heart Pain",
}

# ---- Extract symptoms from free text ----
def extract_symptoms(text):
    text = text.lower()
    words = re.split(r',| and |;', text)
    return [w.strip() for w in words if w.strip()]

# ---- Map user symptoms to dataset columns ----
def map_symptoms(user_input, symptom_columns, keyword_map, cutoff=0.8):
    mapped = {}
    unmatched = []
    for symptom in user_input:
        sym_lower = symptom.lower()
        if sym_lower in keyword_map:
            col_name = keyword_map[sym_lower]
            mapped[col_name] = symptom
        else:
            match = get_close_matches(sym_lower, [s.lower() for s in symptom_columns], n=1, cutoff=cutoff)
            if match:
                col_name = next(s for s in symptom_columns if s.lower() == match[0])
                mapped[col_name] = symptom
            else:
                unmatched.append(symptom)
    return mapped, unmatched

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    unmatched = []

    if request.method == "POST":
        user_text = request.form.get("symptoms")
        user_symptoms = extract_symptoms(user_text)

        mapped_symptoms, unmatched = map_symptoms(user_symptoms, symptom_columns, keyword_map)

        # ---- Disease Match Calculation ----
        disease_scores = []
        for idx, row in data.iterrows():
            matched_count = sum([1 for col in mapped_symptoms if row[col] == 1])
            total_input = len(mapped_symptoms)
            if total_input > 0:
                match_percentage = matched_count / total_input
                if match_percentage > 0:
                    disease_scores.append((match_percentage, row))

        disease_scores.sort(reverse=True, key=lambda x: x[0])

        # ---- Collect Recommendations ----
        recommendations = []
        if disease_scores:
            for score, row in disease_scores[:3]:  # Top 3 results
                recommendations.append({
                    "disease": row["Disease"],
                    "match": f"{score*100:.0f}%",
                    "precautions": row["Precautions"],
                    "medicines": row["Medication"]
                })

        # ---- Per-symptom recommendations ----
        symptom_recommendations = []
        for col, symptom in mapped_symptoms.items():
            matching_rows = data[data[col] == 1]
            if not matching_rows.empty:
                row = matching_rows.iloc[0]
                symptom_recommendations.append({
                    "symptom": symptom,
                    "precaution": str(row["Precautions"]),
                    "medicine": str(row["Medication"])
                })

        result = {
            "recommendations": recommendations,
            "symptom_recommendations": symptom_recommendations
        }

    return render_template("index.html", result=result, unmatched=unmatched)

if __name__ == "__main__":
    app.run(debug=True)
