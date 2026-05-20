import streamlit as st
import pandas as pd
import joblib
import os
import glob

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CardioSense | Heart Risk Predictor",
    page_icon="❤️",
    layout="centered",
)

# ─── CUSTOM CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Root Palette ── */
:root {
    --bg:        #0a0c10;
    --surface:   #121520;
    --card:      #181d28;
    --border:    #1f2535;
    --accent:    #e8394d;
    --accent2:   #ff6b6b;
    --glow:      rgba(232,57,77,0.18);
    --text:      #eef0f5;
    --muted:     #7a8099;
    --success:   #2dd4a0;
    --warning:   #ff9f43;
}

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 1.5rem 4rem !important; max-width: 800px !important; }

/* ── Animated hero header ── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    position: relative;
}
.hero-pulse {
    display: inline-block;
    font-size: 3.2rem;
    animation: heartbeat 1.4s ease-in-out infinite;
}
@keyframes heartbeat {
    0%,100% { transform: scale(1);   }
    14%      { transform: scale(1.18);}
    28%      { transform: scale(1);   }
    42%      { transform: scale(1.12);}
    70%      { transform: scale(1);   }
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.6rem;
    letter-spacing: -0.03em;
    margin: 0.4rem 0 0.2rem;
    background: linear-gradient(135deg, #e8394d 0%, #ff8c94 60%, #ffb3b7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero p {
    color: var(--muted);
    font-size: 1rem;
    font-weight: 300;
    letter-spacing: 0.02em;
    margin: 0;
}
.hero-line {
    width: 60px; height: 3px;
    background: linear-gradient(90deg, var(--accent), transparent);
    border-radius: 2px;
    margin: 1rem auto 0;
}

/* ── Section labels ── */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--accent);
    margin: 2rem 0 0.6rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── Card wrapper ── */
.stform-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 32px rgba(0,0,0,0.35);
    position: relative;
    overflow: hidden;
}
.stform-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent) 0%, transparent 70%);
}

/* ── Input widget overrides ── */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] input,
div[data-baseweb="textarea"] textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}
div[data-baseweb="select"] > div:focus-within,
div[data-baseweb="input"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--glow) !important;
}

/* Slider track */
.stSlider [data-baseweb="slider"] [role="slider"] {
    background: var(--accent) !important;
    border-color: var(--accent) !important;
}
.stSlider [data-baseweb="slider"] [data-testid="stSliderTrackFill"] {
    background: linear-gradient(90deg, var(--accent), var(--accent2)) !important;
}

/* Number input */
.stNumberInput input { text-align: center !important; }

/* Labels */
label, .stSelectbox label, .stSlider label, .stNumberInput label {
    font-size: 0.83rem !important;
    font-weight: 500 !important;
    color: var(--muted) !important;
    letter-spacing: 0.01em !important;
}

/* ── Predict button ── */
div.stButton > button {
    width: 100%;
    padding: 0.85rem 2rem;
    background: linear-gradient(135deg, #c9253a, #e8394d, #ff6b6b) !important;
    background-size: 200% auto !important;
    color: #fff !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase;
    border: none !important;
    border-radius: 12px !important;
    cursor: pointer;
    transition: background-position 0.4s, transform 0.15s, box-shadow 0.3s !important;
    box-shadow: 0 4px 20px rgba(232,57,77,0.4) !important;
    margin-top: 1.4rem !important;
}
div.stButton > button:hover {
    background-position: right center !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(232,57,77,0.55) !important;
}
div.stButton > button:active { transform: translateY(0) !important; }

/* ── Risk result box ── */
.result-box {
    border-radius: 16px;
    padding: 2rem 1.8rem;
    text-align: center;
    margin-top: 1.6rem;
    animation: fadeIn 0.5s ease;
    position: relative;
    overflow: hidden;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
.result-box.high {
    background: linear-gradient(135deg, #1e0a0d, #2d0f14);
    border: 1px solid rgba(232,57,77,0.4);
    box-shadow: 0 0 40px rgba(232,57,77,0.15);
}
.result-box.low {
    background: linear-gradient(135deg, #071a13, #0b2a1f);
    border: 1px solid rgba(45,212,160,0.35);
    box-shadow: 0 0 40px rgba(45,212,160,0.12);
}
.result-icon { font-size: 3rem; margin-bottom: 0.6rem; display: block; }
.result-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.7rem;
    font-weight: 800;
    margin: 0 0 0.4rem;
}
.result-title.high { color: #e8394d; }
.result-title.low  { color: #2dd4a0; }
.result-subtitle {
    font-size: 0.9rem;
    color: var(--muted);
    font-weight: 300;
    max-width: 340px;
    margin: 0 auto;
}

/* ── Metric pills ── */
.metric-row {
    display: flex; gap: 10px; flex-wrap: wrap;
    margin: 1.2rem 0 0.4rem;
    justify-content: center;
}
.metric-pill {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.45rem 0.9rem;
    font-size: 0.78rem;
    color: var(--muted);
}
.metric-pill span { color: var(--text); font-weight: 600; margin-left: 4px; }

/* ── Progress / Risk Meter ── */
.risk-meter-wrap { margin: 1rem 0 0; }
.risk-meter-label {
    display: flex; justify-content: space-between;
    font-size: 0.75rem; color: var(--muted); margin-bottom: 6px;
}
.risk-meter-bar {
    width: 100%; height: 8px;
    background: var(--border);
    border-radius: 4px; overflow: hidden;
}
.risk-meter-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 1s ease;
}
.risk-meter-fill.high {
    background: linear-gradient(90deg, #e8394d, #ff6b6b);
    box-shadow: 0 0 12px rgba(232,57,77,0.5);
}
.risk-meter-fill.low {
    background: linear-gradient(90deg, #2dd4a0, #4dffd9);
    box-shadow: 0 0 12px rgba(45,212,160,0.5);
}

/* ── Disclaimer ── */
.disclaimer {
    text-align: center;
    font-size: 0.72rem;
    color: var(--muted);
    margin-top: 2.5rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border);
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)


# ─── HELPER ───────────────────────────────────────────────────────────────────
def find_file(preferred_names, keywords):
    for name in preferred_names:
        if os.path.exists(name):
            return name
    for f in glob.glob("*.pkl"):
        low = f.lower()
        for kw in keywords:
            if kw in low:
                return f
    return None


# ─── LOAD ASSETS ──────────────────────────────────────────────────────────────
model_file = find_file(
    ["knn_heart_model.pkl", "KNN_heart (1).pkl", "KNN_heart.pkl", "model.pkl"],
    ["knn", "heart", "model"])
scaler_file = find_file(
    ["heart_scaler.pkl", "scaler.pkl", "scaler.sav"],
    ["scaler"])
columns_file = find_file(
    ["heart_columns.pkl", "columns.pkl"],
    ["column", "columns"])

# ─── HERO HEADER ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-pulse">❤️</div>
    <h1>CardioSense</h1>
    <p>Heart Stroke Prediction by Pritam</p>
    <div class="hero-line"></div>
</div>
""", unsafe_allow_html=True)

# ─── MISSING FILES GUARD ──────────────────────────────────────────────────────
if not model_file or not scaler_file or not columns_file:
    st.markdown("""
    <div class="stform-card" style="border-color:#e8394d44; text-align:center;">
        <div style="font-size:2rem;margin-bottom:.6rem;">🔍</div>
        <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;color:#e8394d;margin-bottom:.5rem;">
            Model files not found</div>
        <div style="color:#7a8099;font-size:.85rem;">
            Place <code>knn_heart_model.pkl</code>, <code>scaler.pkl</code>, 
            and <code>columns.pkl</code> in the same folder as this app.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

try:
    model = joblib.load(model_file)
    scaler = joblib.load(scaler_file)
    expected_columns = joblib.load(columns_file)
    if not isinstance(expected_columns, (list, tuple)):
        expected_columns = list(expected_columns)
except Exception as e:
    st.error(f"Failed to load model resources: {e}")
    st.stop()

# ─── FORM ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">👤 Personal Information</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    age = st.slider("Age", 18, 100, 40)
with col2:
    sex = st.selectbox("Biological Sex", ["M", "F"], format_func=lambda x: "Male" if x=="M" else "Female")

st.markdown('<div class="section-label">🩺 Clinical Measurements</div>', unsafe_allow_html=True)
col3, col4 = st.columns(2)
with col3:
    resting_bp  = st.number_input("Resting Blood Pressure (mm Hg)", 80, 200, 120, step=1)
    cholesterol = st.number_input("Cholesterol (mg/dL)", 100, 600, 200, step=1)
with col4:
    max_hr      = st.slider("Max Heart Rate Achieved", 60, 220, 150)
    oldpeak     = st.slider("Oldpeak  (ST Depression)", 0.0, 6.0, 1.0, step=0.1)

st.markdown('<div class="section-label">📋 Diagnostic Details</div>', unsafe_allow_html=True)
col5, col6 = st.columns(2)
with col5:
    chest_pain      = st.selectbox("Chest Pain Type", ["ATA","NAP","TA","ASY"],
                                   help="ATA=Atypical Angina · NAP=Non-Anginal · TA=Typical Angina · ASY=Asymptomatic")
    resting_ecg     = st.selectbox("Resting ECG Result", ["Normal","ST","LVH"])
    exercise_angina = st.selectbox("Exercise-Induced Angina", ["N","Y"],
                                   format_func=lambda x: "No" if x=="N" else "Yes")
with col6:
    fasting_bs = st.selectbox("Fasting Blood Sugar > 120 mg/dL", [0,1],
                               format_func=lambda x: "No (≤120)" if x==0 else "Yes (>120)")
    st_slope   = st.selectbox("ST Slope", ["Up","Flat","Down"])

# ─── PREDICT ──────────────────────────────────────────────────────────────────
if st.button("⚡  Analyse My Risk"):
    raw = {
        'Age': age, 'RestingBP': resting_bp, 'Cholesterol': cholesterol,
        'FastingBS': fasting_bs, 'MaxHR': max_hr, 'Oldpeak': oldpeak,
        'Sex': sex, 'ChestPainType': chest_pain, 'RestingECG': resting_ecg,
        'ExerciseAngina': exercise_angina, 'ST_Slope': st_slope,
    }

    input_df = pd.DataFrame([raw])
    cat_cols = ['Sex','ChestPainType','RestingECG','ExerciseAngina','ST_Slope']
    input_df = pd.get_dummies(input_df, columns=cat_cols, prefix_sep='_')

    for col in expected_columns:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[expected_columns]

    try:
        scaled_input = scaler.transform(input_df)
        prediction   = model.predict(scaled_input)[0]
        # probability if available
        try:
            proba = model.predict_proba(scaled_input)[0]
            risk_pct = int(round(proba[1] * 100))
        except Exception:
            risk_pct = 85 if int(prediction) == 1 else 18
    except Exception as e:
        st.error(f"Prediction failed: {e}")
        st.stop()

    # ── Result card ──
    if int(prediction) == 1:
        st.markdown(f"""
        <div class="result-box high">
            <span class="result-icon">⚠️</span>
            <div class="result-title high">High Risk Detected</div>
            <div class="result-subtitle">
                Your profile indicates elevated cardiovascular risk. 
                Please consult a qualified cardiologist at the earliest.
            </div>
            <div class="metric-row">
                <div class="metric-pill">Age <span>{age}</span></div>
                <div class="metric-pill">BP <span>{resting_bp} mm Hg</span></div>
                <div class="metric-pill">Cholesterol <span>{cholesterol} mg/dL</span></div>
                <div class="metric-pill">Max HR <span>{max_hr}</span></div>
            </div>
            <div class="risk-meter-wrap">
                <div class="risk-meter-label"><span>Low</span><span>Risk Score: {risk_pct}%</span><span>High</span></div>
                <div class="risk-meter-bar">
                    <div class="risk-meter-fill high" style="width:{risk_pct}%"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-box low">
            <span class="result-icon">✅</span>
            <div class="result-title low">Low Risk — You're Doing Well</div>
            <div class="result-subtitle">
                Your profile shows a lower likelihood of heart disease.
                Keep maintaining a healthy lifestyle and get regular check-ups.
            </div>
            <div class="metric-row">
                <div class="metric-pill">Age <span>{age}</span></div>
                <div class="metric-pill">BP <span>{resting_bp} mm Hg</span></div>
                <div class="metric-pill">Cholesterol <span>{cholesterol} mg/dL</span></div>
                <div class="metric-pill">Max HR <span>{max_hr}</span></div>
            </div>
            <div class="risk-meter-wrap">
                <div class="risk-meter-label"><span>Low</span><span>Risk Score: {risk_pct}%</span><span>High</span></div>
                <div class="risk-meter-bar">
                    <div class="risk-meter-fill low" style="width:{risk_pct}%"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="disclaimer">
    ⚕️ &nbsp;This tool is for <strong>educational purposes only</strong> and does not constitute 
    medical advice.<br>Always consult a licensed healthcare professional for diagnosis and treatment.
    <br><br>
    Built with 🩺 by <strong>Pritam</strong> &nbsp;·&nbsp; Powered by KNN + Streamlit
</div>
""", unsafe_allow_html=True)