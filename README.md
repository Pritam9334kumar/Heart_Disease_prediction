# ❤️ Heart Disease Prediction App

A professional Machine Learning web application built using Python and Streamlit to predict the likelihood of heart disease based on medical parameters.

---

## 🚀 Project Overview

This project uses a trained Machine Learning model to analyze patient health data and predict potential heart disease risk.

The application provides:

* Interactive web interface using Streamlit
* Real-time heart disease prediction
* User-friendly medical input form
* Pre-trained ML model integration
* Fast and lightweight deployment

---

## 🛠️ Tech Stack

* Python
* Streamlit
* Scikit-learn
* Pandas
* NumPy
* Joblib

---

## 📂 Project Structure

```bash
project_folder/
│
├── app.py
├── requirements.txt
├── README.md
│
├── knn_heart_model.pkl
├── scaler.pkl
├── columns.pkl
```

---

## 📦 Required Model Files

Before running the application, place the trained model and preprocessing files inside the project folder.

### Expected Files

| File                  | Description                    |
| --------------------- | ------------------------------ |
| `knn_heart_model.pkl` | Trained Machine Learning model |
| `scaler.pkl`          | Feature scaling object         |
| `columns.pkl`         | Training feature columns       |

The application also supports alternative file names containing keywords such as:

* `knn`
* `heart`
* `model`
* `scaler`
* `columns`

---

## ⚙️ Installation Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/heart-disease-prediction.git
```

### 2️⃣ Navigate to Project Folder

```bash
cd heart-disease-prediction
```

### 3️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv .venv
```

### 4️⃣ Activate Virtual Environment

#### Windows

```bash
.venv\Scripts\activate
```

#### macOS/Linux

```bash
source .venv/bin/activate
```

---

## 📥 Install Dependencies

Run the following command:

```bash
python -m pip install -r requirements.txt
```

---

## ▶️ Run the Streamlit Application

Start the application using:

```bash
python -m streamlit run app.py
```

After successful execution, the app will be available at:

```text
http://localhost:8501
```

---

## 🌐 Deploy on Streamlit Cloud

This application can be easily deployed using Streamlit Community Cloud.

### Deployment Steps

1. Push the project to GitHub
2. Open Streamlit Community Cloud
3. Connect your GitHub repository
4. Select `app.py` as the main file
5. Click **Deploy**

---

## 📊 Features Used for Prediction

The model predicts heart disease using medical attributes such as:

* Age
* Sex
* Chest Pain Type
* Resting Blood Pressure
* Cholesterol
* Fasting Blood Sugar
* Resting ECG
* Maximum Heart Rate
* Exercise-Induced Angina
* Oldpeak
* ST Slope

---

## 🎯 Future Improvements

* Add multiple ML algorithms
* Improve model accuracy
* Add data visualization dashboard
* Deploy with Docker
* Add authentication system
* Enable PDF report generation

---

## 📸 Preview

Add screenshots of your application here.

---

## 👨‍💻 Author

Developed by Golu Sharma

---

## 📜 License

This project is open-source and available for educational and learning purposes.
