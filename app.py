import streamlit as st
import pandas as pd
import joblib
import os
import glob


def find_file(preferred_names, keywords):
    # Try preferred names first
    for name in preferred_names:
        if os.path.exists(name):
            return name
    # Fallback: find any .pkl file that contains one of the keywords
    for f in glob.glob("*.pkl"):
        low = f.lower()
        for kw in keywords:
            if kw in low:
                return f
    return None


# Locate model, scaler and columns files (flexible to different filenames)
model_file = find_file([
    "knn_heart_model.pkl",
    "KNN_heart (1).pkl",
    "KNN_heart.pkl",
    "model.pkl",
], ["knn", "heart", "model"])
scaler_file = find_file([
    "heart_scaler.pkl",
    "scaler.pkl",
    "scaler.sav",
], ["scaler"])
columns_file = find_file([
    "heart_columns.pkl",
    "columns.pkl",
    "columns.pkl",
], ["column", "columns"])

if not model_file or not scaler_file or not columns_file:
    st.title("Heart Stroke Prediction by akarsh")
    st.error(
        "Required model/scaler/columns .pkl files not found. Place them in the app folder."
    )
    st.markdown(
        "Expected files (examples): `knn_heart_model.pkl`, `scaler.pkl`, `columns.pkl`"
    )
    st.stop()

try:
    model = joblib.load(model_file)
    scaler = joblib.load(scaler_file)
    expected_columns = joblib.load(columns_file)
except Exception as e:
    st.title("Heart Stroke Prediction by akarsh")
    st.error(f"Failed to load resources: {e}")
    st.stop()

if not isinstance(expected_columns, (list, tuple)):
    # try to coerce numpy array or pandas Index to list
    try:
        expected_columns = list(expected_columns)
    except Exception:
        st.title("Heart Stroke Prediction by akarsh")
        st.error("`columns.pkl` did not contain a list of expected column names.")
        st.stop()

st.title("Heart Stroke Prediction by akarsh")
st.markdown("Provide the following details to check your heart stroke risk:")

# Collect user input
age = st.slider("Age", 18, 100, 40)
sex = st.selectbox("Sex", ["M", "F"])
chest_pain = st.selectbox("Chest Pain Type", ["ATA", "NAP", "TA", "ASY"])
resting_bp = st.number_input("Resting Blood Pressure (mm Hg)", 80, 200, 120)
cholesterol = st.number_input("Cholesterol (mg/dL)", 100, 600, 200)
fasting_bs = st.selectbox("Fasting Blood Sugar > 120 mg/dL", [0, 1])
resting_ecg = st.selectbox("Resting ECG", ["Normal", "ST", "LVH"])
max_hr = st.slider("Max Heart Rate", 60, 220, 150)
exercise_angina = st.selectbox("Exercise-Induced Angina", ["Y", "N"])
oldpeak = st.slider("Oldpeak (ST Depression)", 0.0, 6.0, 1.0)
st_slope = st.selectbox("ST Slope", ["Up", "Flat", "Down"])

# When Predict is clicked
if st.button("Predict"):

    # Build a raw DataFrame with categorical values, then one-hot encode
    raw = {
        'Age': age,
        'RestingBP': resting_bp,
        'Cholesterol': cholesterol,
        'FastingBS': fasting_bs,
        'MaxHR': max_hr,
        'Oldpeak': oldpeak,
        'Sex': sex,
        'ChestPainType': chest_pain,
        'RestingECG': resting_ecg,
        'ExerciseAngina': exercise_angina,
        'ST_Slope': st_slope,
    }

    input_df = pd.DataFrame([raw])
    cat_cols = ['Sex', 'ChestPainType', 'RestingECG', 'ExerciseAngina', 'ST_Slope']
    try:
        input_df = pd.get_dummies(input_df, columns=cat_cols, prefix_sep='_')
    except Exception:
        # If get_dummies fails for any reason, fall back to original approach
        for c in cat_cols:
            val = raw.get(c)
            if val is not None:
                input_df[c + '_' + str(val)] = 1

    # Ensure all expected columns exist
    for col in expected_columns:
        if col not in input_df.columns:
            input_df[col] = 0

    # Reorder columns to the expected order
    input_df = input_df[expected_columns]

    # Scale and predict with error handling
    try:
        scaled_input = scaler.transform(input_df)
        prediction = model.predict(scaled_input)[0]
    except Exception as e:
        st.error(f"Prediction failed: {e}")
        raise

    # Show result
    if int(prediction) == 1:
        st.error("⚠️ High Risk of Heart Disease")
    else:
        st.success("✅ Low Risk of Heart Disease")