# Health-Assistant---Symptom-Checker

# 🩺 Health Assistant - Symptom Checker

A **web-based Health Assistant** built with **Python Flask** that provides **disease predictions**, **precautions**, and **medicine recommendations** based on user-reported symptoms.

---

## 🚀 Features

- Accepts **plain-text symptom input** (e.g., "fever, headache, teeth pain")  
- Matches symptoms with a **preloaded CSV dataset** of diseases  
- Provides **possible diseases** ranked by **match percentage**  
- Shows **precaution advice** and **medicines** for each symptom  
- Alerts users about **unmatched symptoms**  
- Notes: General recommendations; **consult a doctor if symptoms persist**

---

## 🛠 Technology Stack

- **Backend:** Python, Flask  
- **Frontend:** HTML (Jinja2 templates)  
- **Data Handling:** Pandas  
- **Deployment-ready:** Render / PythonAnywhere  
- **Other libraries:** difflib, re, gunicorn (for deployment)

---

## 📁 Project Structure

my-project/
│── app.py # Flask application

│── symptom_disease_150.csv # Dataset of symptoms and diseases

│── requirements.txt # Python dependencies

│── Procfile # Deployment file for Render

│── runtime.txt # Python version for deployment

│── templates/

│ └── index.html # Frontend HTML template

## 👨‍💻 Author

ROHITH A M
- GitHub: https://github.com/ROHITT2108
- LinkedIn: [https://www.linkedin.com/in/rohith-a-m-694497319]
