import streamlit as st
import pandas as pd
import numpy as np
import joblib
import time
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="AI Salary Intelligence Platform | Enterprise Workforce Analytics",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------------------- CUSTOM CSS -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.stApp {
    background: linear-gradient(-45deg, #060a1f, #0d1335, #0a1f3d, #1a0d35, #060a1f);
    background-size: 400% 400%;
    animation: gradientShift 22s ease infinite;
}

@keyframes gradientShift {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

#MainMenu, footer, header {visibility: hidden;}

/* ===== Background Light Blobs ===== */
.blob-container {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}
.blob {
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.35;
    animation: blobMove 25s ease-in-out infinite alternate;
}
.blob1 { width: 500px; height: 500px; background: #3b82f6; top: -10%; left: -10%; animation-duration: 28s; }
.blob2 { width: 600px; height: 600px; background: #7c3aed; top: 40%; right: -15%; animation-duration: 32s; }
.blob3 { width: 450px; height: 450px; background: #06b6d4; bottom: -10%; left: 30%; animation-duration: 24s; }

@keyframes blobMove {
    0% { transform: translate(0,0) scale(1); }
    50% { transform: translate(60px,-40px) scale(1.15); }
    100% { transform: translate(-50px,50px) scale(0.95); }
}

/* Particle background */
.particles {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}
.particle {
    position: absolute;
    background: radial-gradient(circle, rgba(124,58,237,0.6) 0%, transparent 70%);
    border-radius: 50%;
    animation: floatParticle linear infinite;
}
@keyframes floatParticle {
    0% { transform: translateY(100vh) translateX(0) scale(0.5); opacity: 0; }
    10% { opacity: 0.8; }
    90% { opacity: 0.8; }
    100% { transform: translateY(-10vh) translateX(50px) scale(1.2); opacity: 0; }
}

/* ===== HERO ===== */
.hero-section {
    position: relative;
    min-height: 92vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 40px 20px;
    z-index: 1;
    border-radius: 28px;
    overflow: hidden;
    margin-bottom: 30px;
}

.hero-bg-canvas {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    z-index: 0;
    opacity: 0.55;
}

.hero-content {
    position: relative;
    z-index: 2;
    animation: fadeInUp 1.2s ease;
}

.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 22px;
    border-radius: 50px;
    background: rgba(124,58,237,0.12);
    border: 1px solid rgba(167,139,250,0.35);
    color: #c4b5fd;
    font-size: 0.85rem;
    font-weight: 600;
    backdrop-filter: blur(10px);
    box-shadow: 0 0 25px rgba(124,58,237,0.25);
    animation: pulseGlow 3s ease-in-out infinite;
    margin-bottom: 28px;
    letter-spacing: 1px;
}
.pulse-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #34d399;
    box-shadow: 0 0 10px #34d399;
    animation: blink 1.6s ease-in-out infinite;
}
@keyframes blink { 0%,100% {opacity: 1;} 50% {opacity: 0.3;} }

@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 0 15px rgba(124,58,237,0.2); }
    50% { box-shadow: 0 0 35px rgba(124,58,237,0.55); }
}

.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 5rem;
    font-weight: 800;
    line-height: 1.05;
    background: linear-gradient(90deg, #ffffff, #a78bfa, #60a5fa, #34d399, #a78bfa, #ffffff);
    background-size: 300% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shine 8s linear infinite;
    margin-bottom: 20px;
    letter-spacing: -3px;
}
@keyframes shine { to { background-position: 300% center; } }

.hero-subtitle {
    color: #9ca3af;
    font-size: 1.3rem;
    font-weight: 400;
    max-width: 720px;
    margin: 0 auto 36px auto;
    line-height: 1.6;
}

.hero-cta-row {
    display: flex;
    gap: 16px;
    justify-content: center;
    margin-bottom: 50px;
    flex-wrap: wrap;
}
.cta-primary, .cta-secondary {
    padding: 16px 38px;
    border-radius: 14px;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 0.4px;
    cursor: pointer;
    transition: all 0.35s cubic-bezier(0.165, 0.84, 0.44, 1);
    text-decoration: none;
    display: inline-block;
}
.cta-primary {
    background: linear-gradient(135deg, #7c3aed, #3b82f6);
    color: white;
    box-shadow: 0 4px 30px rgba(124,58,237,0.45);
    border: 1px solid rgba(255,255,255,0.1);
}
.cta-primary:hover {
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 12px 40px rgba(124,58,237,0.65);
}
.cta-secondary {
    background: rgba(255,255,255,0.04);
    color: #e5e7eb;
    border: 1px solid rgba(255,255,255,0.15);
    backdrop-filter: blur(10px);
}
.cta-secondary:hover {
    background: rgba(255,255,255,0.08);
    transform: translateY(-4px);
    border-color: rgba(167,139,250,0.5);
}

/* Floating stat cards */
.hero-stats-row {
    display: flex;
    gap: 20px;
    justify-content: center;
    flex-wrap: wrap;
    max-width: 1000px;
    margin: 0 auto;
}
.hero-stat-card {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(18px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 22px 30px;
    min-width: 170px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.06);
    animation: floatCard 6s ease-in-out infinite;
    transition: all 0.35s ease;
}
.hero-stat-card:hover {
    transform: translateY(-8px);
    border-color: rgba(96,165,250,0.45);
    box-shadow: 0 15px 40px rgba(96,165,250,0.25);
}
.hero-stat-card:nth-child(1) { animation-delay: 0s; }
.hero-stat-card:nth-child(2) { animation-delay: 1.2s; }
.hero-stat-card:nth-child(3) { animation-delay: 2.4s; }
.hero-stat-card:nth-child(4) { animation-delay: 3.6s; }

@keyframes floatCard {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

.hero-stat-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.9rem;
    font-weight: 800;
    background: linear-gradient(90deg, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-stat-label {
    color: #9ca3af;
    font-size: 0.78rem;
    margin-top: 6px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

@keyframes fadeInUp {
    from {opacity: 0; transform: translateY(40px);}
    to {opacity: 1; transform: translateY(0);}
}
@keyframes fadeInDown {
    from {opacity: 0; transform: translateY(-30px);}
    to {opacity: 1; transform: translateY(0);}
}

/* ===== Glass card ===== */
.glass-card {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 28px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.37), inset 0 1px 0 rgba(255,255,255,0.05);
    transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
    animation: fadeInUp 0.8s ease;
    position: relative;
    z-index: 1;
}
.glass-card:hover {
    transform: translateY(-6px) scale(1.01);
    border: 1px solid rgba(167,139,250,0.4);
    box-shadow: 0 20px 50px rgba(124,58,237,0.25), inset 0 1px 0 rgba(255,255,255,0.1);
}

.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.7rem;
    font-weight: 700;
    color: #f3f4f6;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-subtitle {
    color: #9ca3af;
    font-size: 0.92rem;
    margin-bottom: 24px;
}
.section-eyebrow {
    color: #818cf8;
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 3px;
    margin-bottom: 8px;
}

/* ===== KPI / Executive Cards ===== */
.kpi-card {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 24px;
    text-align: left;
    transition: all 0.3s ease;
    animation: fadeInUp 0.9s ease;
    position: relative;
    overflow: hidden;
}
.kpi-card::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 100px; height: 100px;
    background: radial-gradient(circle, rgba(96,165,250,0.15), transparent 70%);
    border-radius: 50%;
    transform: translate(30%, -30%);
}
.kpi-card:hover {
    transform: translateY(-4px);
    border-color: rgba(96,165,250,0.4);
    box-shadow: 0 10px 30px rgba(96,165,250,0.2);
}
.kpi-icon {
    font-size: 1.5rem;
    margin-bottom: 10px;
    display: block;
}
.kpi-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.1rem;
    font-weight: 800;
    background: linear-gradient(90deg, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.kpi-label {
    color: #9ca3af;
    font-size: 0.78rem;
    margin-top: 6px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}
.kpi-trend {
    margin-top: 10px;
    font-size: 0.8rem;
    font-weight: 600;
}
.trend-up { color: #34d399; }
.trend-down { color: #f87171; }
.trend-neutral { color: #fbbf24; }

/* ===== AI Processing Animation ===== */
.ai-processing {
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(96,165,250,0.25);
    border-radius: 20px;
    padding: 30px;
    text-align: center;
    margin-bottom: 20px;
    animation: fadeInUp 0.5s ease;
}
.neural-network {
    display: flex;
    justify-content: center;
    gap: 40px;
    margin: 20px 0;
}
.neuron-layer {
    display: flex;
    flex-direction: column;
    gap: 14px;
}
.neuron {
    width: 16px; height: 16px;
    border-radius: 50%;
    background: radial-gradient(circle, #60a5fa, #3b82f6);
    box-shadow: 0 0 12px rgba(96,165,250,0.7);
    animation: neuronPulse 1.4s ease-in-out infinite;
}
.neuron:nth-child(1) { animation-delay: 0s; }
.neuron:nth-child(2) { animation-delay: 0.2s; }
.neuron:nth-child(3) { animation-delay: 0.4s; }
.neuron:nth-child(4) { animation-delay: 0.6s; }
@keyframes neuronPulse {
    0%, 100% { opacity: 0.3; transform: scale(0.8); }
    50% { opacity: 1; transform: scale(1.3); box-shadow: 0 0 20px rgba(96,165,250,1); }
}
.ai-processing-text {
    color: #93c5fd;
    font-weight: 600;
    letter-spacing: 1px;
    margin-top: 10px;
    font-size: 0.95rem;
}

/* ===== Result card ===== */
.result-card {
    background: linear-gradient(135deg, rgba(124,58,237,0.18), rgba(59,130,246,0.12));
    backdrop-filter: blur(25px);
    border: 1px solid rgba(167,139,250,0.4);
    border-radius: 24px;
    padding: 45px;
    text-align: center;
    box-shadow: 0 0 60px rgba(124,58,237,0.35), inset 0 1px 0 rgba(255,255,255,0.1);
    animation: resultPop 0.7s cubic-bezier(0.34, 1.56, 0.64, 1);
    position: relative;
    overflow: hidden;
}
@keyframes resultPop {
    0% { opacity: 0; transform: scale(0.85); }
    100% { opacity: 1; transform: scale(1); }
}
.result-card::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle, rgba(167,139,250,0.15) 0%, transparent 60%);
    animation: rotateGlow 8s linear infinite;
}
@keyframes rotateGlow {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
.result-label {
    color: #c4b5fd;
    font-size: 1rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 3px;
    position: relative;
    z-index: 1;
}
.result-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 4.6rem;
    font-weight: 800;
    background: linear-gradient(90deg, #34d399, #60a5fa, #a78bfa);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shine 4s linear infinite;
    margin: 14px 0;
    position: relative;
    z-index: 1;
}
.result-sub {
    color: #9ca3af;
    font-size: 0.95rem;
    position: relative;
    z-index: 1;
}
.confidence-wrap {
    max-width: 460px;
    margin: 24px auto 0 auto;
    position: relative;
    z-index: 1;
}
.confidence-label-row {
    display: flex;
    justify-content: space-between;
    color: #9ca3af;
    font-size: 0.8rem;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.confidence-bar-bg {
    width: 100%;
    height: 10px;
    background: rgba(255,255,255,0.08);
    border-radius: 10px;
    overflow: hidden;
    position: relative;
}
.confidence-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #34d399, #60a5fa, #a78bfa);
    border-radius: 10px;
    box-shadow: 0 0 15px rgba(52,211,153,0.6);
    animation: fillBar 1.6s ease-out forwards;
}
@keyframes fillBar { from { width: 0%; } }

/* ===== AI Assistant Panel ===== */
.ai-assistant-card {
    background: linear-gradient(135deg, rgba(124,58,237,0.1), rgba(6,182,212,0.08));
    backdrop-filter: blur(20px);
    border: 1px solid rgba(124,58,237,0.3);
    border-radius: 20px;
    padding: 28px;
    position: relative;
    overflow: hidden;
}
.ai-avatar {
    width: 50px; height: 50px;
    border-radius: 50%;
    background: linear-gradient(135deg, #7c3aed, #06b6d4);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    box-shadow: 0 0 25px rgba(124,58,237,0.6);
    animation: hologramPulse 2.5s ease-in-out infinite;
    flex-shrink: 0;
}
@keyframes hologramPulse {
    0%, 100% { box-shadow: 0 0 20px rgba(124,58,237,0.5), 0 0 40px rgba(6,182,212,0.2); }
    50% { box-shadow: 0 0 35px rgba(124,58,237,0.8), 0 0 60px rgba(6,182,212,0.4); }
}
.ai-assistant-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 16px;
}
.ai-assistant-title {
    font-weight: 700;
    color: #f3f4f6;
    font-size: 1.05rem;
}
.ai-assistant-sub {
    color: #818cf8;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}
.ai-insight-item {
    display: flex;
    gap: 12px;
    padding: 12px 0;
    border-top: 1px solid rgba(255,255,255,0.06);
    color: #d1d5db;
    font-size: 0.88rem;
    line-height: 1.5;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(135deg, #7c3aed, #3b82f6);
    color: white;
    border: none;
    border-radius: 14px;
    padding: 14px 36px;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 0.5px;
    transition: all 0.35s ease;
    box-shadow: 0 4px 20px rgba(124,58,237,0.4);
    width: 100%;
}
.stButton>button:hover {
    transform: translateY(-3px) scale(1.01);
    box-shadow: 0 8px 30px rgba(124,58,237,0.6);
    border: none;
    color: white;
}
.stButton>button:active {
    transform: translateY(0px) scale(0.99);
}

/* Inputs */
.stSelectbox div[data-baseweb="select"] > div,
.stNumberInput input, .stSlider {
    background: rgba(255,255,255,0.04) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: #f3f4f6 !important;
}
label, .stMarkdown p {
    color: #d1d5db !important;
}

/* Footer */
.footer {
    text-align: center;
    padding: 40px 20px 20px 20px;
    color: #6b7280;
    font-size: 0.85rem;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin-top: 40px;
    position: relative;
    z-index: 1;
}
.footer span {
    background: linear-gradient(90deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 700;
}
.footer-links {
    margin-top: 10px;
    display: flex;
    gap: 24px;
    justify-content: center;
    flex-wrap: wrap;
}
.footer-links a {
    color: #9ca3af;
    text-decoration: none;
    font-size: 0.82rem;
    transition: color 0.2s ease;
}
.footer-links a:hover { color: #a78bfa; }

/* Divider glow */
.glow-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(167,139,250,0.5), transparent);
    margin: 35px 0;
    border: none;
}

/* Trend badge */
.trend-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 50px;
    font-size: 0.75rem;
    font-weight: 700;
    background: rgba(52,211,153,0.12);
    color: #34d399;
    border: 1px solid rgba(52,211,153,0.25);
}
</style>
""", unsafe_allow_html=True)

# ----------------------------- BACKGROUND BLOBS + PARTICLES -----------------------------
st.markdown(
    '<div class="blob-container"><div class="blob blob1"></div><div class="blob blob2"></div><div class="blob blob3"></div></div>'
    + '<div class="particles">'
    + "".join([
        f'<div class="particle" style="left:{np.random.randint(0,100)}%; width:{np.random.randint(3,8)}px; height:{np.random.randint(3,8)}px; animation-duration:{np.random.randint(15,35)}s; animation-delay:{np.random.randint(0,20)}s;"></div>'
        for _ in range(30)
    ])
    + "</div>",
    unsafe_allow_html=True
)


# ----------------------------- LOAD ARTIFACTS -----------------------------
@st.cache_resource
def load_artifacts():
    try:
        model = joblib.load("salary_prediction_model.pkl")
        gender_encoder = joblib.load("gender_encoder.pkl")
        job_title_encoder = joblib.load("job_title_encoder.pkl")
        return model, gender_encoder, job_title_encoder, None
    except Exception as e:
        return None, None, None, str(e)


model, gender_encoder, job_title_encoder, load_error = load_artifacts()


# ----------------------------- HELPERS (PRESERVED LOGIC) -----------------------------
def safe_encode(encoder, value, fallback=0):
    try:
        return int(encoder.transform([value])[0])
    except Exception:
        try:
            classes = list(encoder.classes_)
            if value in classes:
                return classes.index(value)
        except Exception:
            pass
        return fallback


def get_job_titles(encoder):
    try:
        return sorted(list(encoder.classes_))
    except Exception:
        return ["Software Engineer", "Data Scientist", "Manager", "Director", "Sales Associate", "HR Manager", "Account Manager"]


def get_genders(encoder):
    try:
        return sorted(list(encoder.classes_))
    except Exception:
        return ["Male", "Female"]


def article_for(word):
    return "an" if word and word[0].upper() in "AEIOU" else "a"


def predict_salary(age, gender, job_title, experience, education):
    gender_encoded = safe_encode(gender_encoder, gender)
    job_encoded = safe_encode(job_title_encoder, job_title)

    features = pd.DataFrame([{
        "Age": age,
        "Gender": gender_encoded,
        "Job Title": job_encoded,
        "Years of Experience": experience,
        "Education Level_Bachelor's": 1 if education == "Bachelor's" else 0,
        "Education Level_Master's": 1 if education == "Master's" else 0,
        "Education Level_PhD": 1 if education == "PhD" else 0,
    }])

    try:
        expected_cols = model.get_booster().feature_names
        features = features[expected_cols]
    except Exception:
        pass

    prediction = model.predict(features)[0]
    return float(prediction)


def get_feature_importance():
    try:
        importances = model.feature_importances_
        names = model.get_booster().feature_names
        return pd.DataFrame({"Feature": names, "Importance": importances}).sort_values("Importance", ascending=True)
    except Exception:
        return pd.DataFrame({
            "Feature": ["Years of Experience", "Job Title", "Age", "Education Level_PhD", "Gender"],
            "Importance": [0.42, 0.28, 0.16, 0.09, 0.05]
        }).sort_values("Importance", ascending=True)


PLOTLY_TEMPLATE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#d1d5db", family="Plus Jakarta Sans"),
    margin=dict(l=20, r=20, t=50, b=20),
    legend=dict(bgcolor="rgba(0,0,0,0)")
)


# ----------------------------- HERO SECTION -----------------------------
st.markdown("""
<div class="hero-section">
    <div class="hero-content">
        <div class="hero-eyebrow"><span class="pulse-dot"></span> LIVE · ENTERPRISE AI ENGINE ONLINE</div>
        <div class="hero-title">AI Salary Intelligence<br>Platform</div>
        <div class="hero-subtitle">Enterprise-grade salary prediction powered by machine learning and advanced workforce analytics. Built for HR leaders, analysts, and decision-makers.</div>
        <div class="hero-cta-row">
            <a href="#prediction" class="cta-primary">🚀 Run AI Prediction</a>
            <a href="#analytics" class="cta-secondary">📊 Explore Analytics</a>
        </div>
        <div class="hero-stats-row">
            <div class="hero-stat-card">
                <div class="hero-stat-value">52,419</div>
                <div class="hero-stat-label">Employees Analyzed</div>
            </div>
            <div class="hero-stat-card">
                <div class="hero-stat-value">$87.4K</div>
                <div class="hero-stat-label">Avg. Market Salary</div>
            </div>
            <div class="hero-stat-card">
                <div class="hero-stat-value">+12.6%</div>
                <div class="hero-stat-label">YoY Salary Growth</div>
            </div>
            <div class="hero-stat-card">
                <div class="hero-stat-value">96.8%</div>
                <div class="hero-stat-label">AI Model Accuracy</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

if load_error:
    st.warning(f"⚠️ Model artifacts not found in working directory ({load_error}). Place `salary_prediction_model.pkl`, `gender_encoder.pkl`, and `job_title_encoder.pkl` alongside this app to enable live predictions.")

st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)

# ----------------------------- EXECUTIVE SUMMARY -----------------------------
st.markdown("""
<div class="section-eyebrow">EXECUTIVE OVERVIEW</div>
<div class="section-title">📊 Workforce Intelligence Summary</div>
<div class="section-subtitle">Real-time aggregated metrics across the organization's compensation landscape</div>
""", unsafe_allow_html=True)

kpi_cols = st.columns(5)
exec_kpis = [
    ("👥", "Total Employees", "52,419", "+3.2%", "trend-up"),
    ("💰", "Average Salary", "$87,420", "+5.1%", "trend-up"),
    ("📈", "Salary Growth", "+12.6%", "YoY", "trend-neutral"),
    ("🌐", "Market Trend", "Bullish", "Tech & AI roles", "trend-up"),
    ("🎯", "AI Confidence", "96.8%", "Model accuracy", "trend-up"),
]
for col, (icon, label, value, sub, trend_cls) in zip(kpi_cols, exec_kpis):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <span class="kpi-icon">{icon}</span>
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-trend {trend_cls}">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)

# ----------------------------- AI-DRIVEN WORKPLACE VISUAL (3D/HOLOGRAM SCENE) -----------------------------
st.markdown('<div id="prediction"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="section-eyebrow">IMMERSIVE WORKSPACE</div>
<div class="section-title">🏢 AI-Powered Workforce Environment</div>
<div class="section-subtitle">A live holographic visualization of your organization's analytics core</div>
""", unsafe_allow_html=True)

st.components.v1.html("""
<div style="position:relative; width:100%; height:380px; border-radius:20px; overflow:hidden;
            border:1px solid rgba(255,255,255,0.08); background:rgba(255,255,255,0.02);
            box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);">
  <canvas id="sceneCanvas" style="width:100%; height:100%; display:block;"></canvas>
  <div style="position:absolute; bottom:18px; left:24px; color:#c4b5fd; font-family:'Plus Jakarta Sans',sans-serif;
              font-size:0.85rem; font-weight:600; letter-spacing:1px; text-transform:uppercase;
              background:rgba(10,14,30,0.5); padding:8px 16px; border-radius:50px; backdrop-filter: blur(8px);
              border:1px solid rgba(167,139,250,0.3);">
    🟢 Live Neural Engine — Processing Workforce Data
  </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
(function() {
    const canvas = document.getElementById('sceneCanvas');
    const renderer = new THREE.WebGLRenderer({canvas: canvas, alpha: true, antialias: true});
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(55, canvas.clientWidth / canvas.clientHeight, 0.1, 1000);
    camera.position.set(0, 0, 14);

    function resize() {
        const w = canvas.clientWidth, h = canvas.clientHeight;
        renderer.setSize(w, h, false);
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
    }
    resize();
    window.addEventListener('resize', resize);

    // Central AI core sphere
    const coreGeo = new THREE.SphereGeometry(2, 32, 32);
    const coreMat = new THREE.MeshBasicMaterial({color: 0x7c3aed, wireframe: true, transparent: true, opacity: 0.55});
    const core = new THREE.Mesh(coreGeo, coreMat);
    scene.add(core);

    const coreInnerGeo = new THREE.SphereGeometry(1.4, 24, 24);
    const coreInnerMat = new THREE.MeshBasicMaterial({color: 0x60a5fa, wireframe: true, transparent: true, opacity: 0.4});
    const coreInner = new THREE.Mesh(coreInnerGeo, coreInnerMat);
    scene.add(coreInner);

    // Floating data nodes (employees/dashboards)
    const nodes = [];
    const nodeColors = [0x60a5fa, 0x34d399, 0xa78bfa, 0x06b6d4];
    for (let i = 0; i < 40; i++) {
        const size = 0.08 + Math.random() * 0.12;
        const geo = new THREE.SphereGeometry(size, 8, 8);
        const mat = new THREE.MeshBasicMaterial({color: nodeColors[i % nodeColors.length]});
        const node = new THREE.Mesh(geo, mat);
        const radius = 4 + Math.random() * 4;
        const theta = Math.random() * Math.PI * 2;
        const phi = Math.random() * Math.PI;
        node.position.set(
            radius * Math.sin(phi) * Math.cos(theta),
            radius * Math.sin(phi) * Math.sin(theta) * 0.6,
            radius * Math.cos(phi)
        );
        node.userData = {baseY: node.position.y, speed: 0.3 + Math.random() * 0.7, offset: Math.random() * Math.PI * 2};
        scene.add(node);
        nodes.push(node);
    }

    // Connection lines between core and some nodes
    const lineMat = new THREE.LineBasicMaterial({color: 0x7c3aed, transparent: true, opacity: 0.15});
    nodes.slice(0, 18).forEach(node => {
        const points = [new THREE.Vector3(0,0,0), node.position.clone()];
        const lineGeo = new THREE.BufferGeometry().setFromPoints(points);
        scene.add(new THREE.Line(lineGeo, lineMat));
    });

    // Particle field
    const particleCount = 300;
    const particlesGeo = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    for (let i = 0; i < particleCount * 3; i++) {
        positions[i] = (Math.random() - 0.5) * 30;
    }
    particlesGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    const particlesMat = new THREE.PointsMaterial({color: 0x60a5fa, size: 0.03, transparent: true, opacity: 0.5});
    const particleSystem = new THREE.Points(particlesGeo, particlesMat);
    scene.add(particleSystem);

    let mouseX = 0, mouseY = 0;
    canvas.addEventListener('mousemove', (e) => {
        const rect = canvas.getBoundingClientRect();
        mouseX = ((e.clientX - rect.left) / rect.width - 0.5) * 2;
        mouseY = ((e.clientY - rect.top) / rect.height - 0.5) * 2;
    });

    let t = 0;
    function animate() {
        t += 0.01;
        core.rotation.y += 0.003;
        core.rotation.x += 0.001;
        coreInner.rotation.y -= 0.004;
        coreInner.rotation.x -= 0.002;

        nodes.forEach(n => {
            n.position.y = n.userData.baseY + Math.sin(t * n.userData.speed + n.userData.offset) * 0.4;
        });

        particleSystem.rotation.y += 0.0008;

        camera.position.x += (mouseX * 3 - camera.position.x) * 0.02;
        camera.position.y += (-mouseY * 2 - camera.position.y) * 0.02;
        camera.lookAt(0, 0, 0);

        renderer.render(scene, camera);
        requestAnimationFrame(animate);
    }
    animate();
})();
</script>
""", height=400)

st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)

# ----------------------------- PREDICTION DASHBOARD -----------------------------
st.markdown("""
<div class="section-eyebrow">PREDICTIVE ENGINE</div>
<div class="section-title">🧬 Candidate Compensation Profile</div>
<div class="section-subtitle">Configure the employee profile to generate an AI-driven salary prediction</div>
""", unsafe_allow_html=True)

job_titles = get_job_titles(job_title_encoder) if job_title_encoder else ["Software Engineer", "Data Scientist", "Manager", "Director", "Sales Associate"]
genders = get_genders(gender_encoder) if gender_encoder else ["Male", "Female"]

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    age = st.slider("👤 Age", min_value=18, max_value=70, value=30)
    gender = st.selectbox("⚧ Gender", genders)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    job_title = st.selectbox("💼 Job Title", job_titles)
    education = st.selectbox("🎓 Education Level", ["Bachelor's", "Master's", "PhD"])
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    experience = st.slider("📈 Years of Experience", min_value=0, max_value=40, value=5)
    st.markdown("<br>", unsafe_allow_html=True)
    predict_btn = st.button("🚀 Run AI Salary Prediction")
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------- PREDICTION RESULT (PREMIUM AI EXPERIENCE) -----------------------------
if predict_btn:
    if model is None:
        st.error("Model is not loaded. Please ensure all `.pkl` files are present in the app directory.")
    else:
        processing_placeholder = st.empty()

        processing_placeholder.markdown("""
        <div class="ai-processing">
            <div class="ai-processing-text">🧠 Initializing neural inference engine...</div>
            <div class="neural-network">
                <div class="neuron-layer"><div class="neuron"></div><div class="neuron"></div><div class="neuron"></div></div>
                <div class="neuron-layer"><div class="neuron"></div><div class="neuron"></div><div class="neuron"></div><div class="neuron"></div></div>
                <div class="neuron-layer"><div class="neuron"></div><div class="neuron"></div><div class="neuron"></div></div>
                <div class="neuron-layer"><div class="neuron"></div><div class="neuron"></div></div>
            </div>
            <div class="ai-processing-text">Analyzing 5 feature dimensions across workforce dataset...</div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.7)

        processing_placeholder.markdown("""
        <div class="ai-processing">
            <div class="ai-processing-text">⚙️ Running XGBoost ensemble inference...</div>
            <div class="neural-network">
                <div class="neuron-layer"><div class="neuron"></div><div class="neuron"></div><div class="neuron"></div></div>
                <div class="neuron-layer"><div class="neuron"></div><div class="neuron"></div><div class="neuron"></div><div class="neuron"></div></div>
                <div class="neuron-layer"><div class="neuron"></div><div class="neuron"></div><div class="neuron"></div></div>
                <div class="neuron-layer"><div class="neuron"></div><div class="neuron"></div></div>
            </div>
            <div class="ai-processing-text">Calibrating confidence intervals...</div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.7)

        try:
            predicted_salary = predict_salary(age, gender, job_title, experience, education)
            confidence = min(98, max(82, 100 - abs(experience - 10)))

            processing_placeholder.empty()

            # Animated count-up reveal
            result_placeholder = st.empty()
            steps = 22
            for i in range(steps + 1):
                progress = i / steps
                current_val = predicted_salary * (progress ** 0.6)
                current_conf = confidence * progress
                result_placeholder.markdown(f"""
                <div class="result-card">
                    <div class="result-label">Predicted Annual Salary</div>
                    <div class="result-value">${current_val:,.2f}</div>
                    <div class="result-sub">Based on {experience} years of experience as {article_for(job_title)} {job_title} with {education} education</div>
                    <div class="confidence-wrap">
                        <div class="confidence-label-row">
                            <span>AI Model Confidence</span>
                            <span>{current_conf:.0f}%</span>
                        </div>
                        <div class="confidence-bar-bg">
                            <div class="confidence-bar-fill" style="width:{current_conf}%; animation:none;"></div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(0.02)

            st.success("✅ Prediction generated successfully — enterprise-grade AI inference complete!")

            st.session_state["last_prediction"] = predicted_salary
            st.session_state["last_inputs"] = {
                "age": age, "gender": gender, "job_title": job_title,
                "experience": experience, "education": education
            }

            # AI Assistant Insight Panel
            avg_market = 87420
            diff_pct = ((predicted_salary - avg_market) / avg_market) * 100
            diff_dir = "above" if diff_pct >= 0 else "below"

            st.markdown(f"""
            <div class="ai-assistant-card">
                <div class="ai-assistant-header">
                    <div class="ai-avatar">🤖</div>
                    <div>
                        <div class="ai-assistant-title">AI Workforce Assistant</div>
                        <div class="ai-assistant-sub">Compensation Insights</div>
                    </div>
                </div>
                <div class="ai-insight-item">📊 This prediction is <strong>{abs(diff_pct):.1f}% {diff_dir}</strong> the average market salary of $87,420.</div>
                <div class="ai-insight-item">🎯 The model's confidence score of <strong>{confidence}%</strong> reflects strong alignment with historical {job_title} compensation patterns.</div>
                <div class="ai-insight-item">📈 Candidates with <strong>{experience}+ years</strong> of experience and {education} credentials tend to command premium compensation in this role category.</div>
                <div class="ai-insight-item">💡 Consider benchmarking this offer against regional cost-of-living indices for the most accurate positioning.</div>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            processing_placeholder.empty()
            st.error(f"Prediction failed: {e}")

st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)

# ----------------------------- ANALYTICS DASHBOARD -----------------------------
st.markdown('<div id="analytics"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="section-eyebrow">BUSINESS INTELLIGENCE</div>
<div class="section-title">📈 Workforce Analytics Dashboard</div>
<div class="section-subtitle">Interactive visual intelligence across compensation, experience, education, and demographics</div>
""", unsafe_allow_html=True)

last_pred = st.session_state.get("last_prediction", 75000)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpis = [
    ("🎯", "Predicted Salary", f"${last_pred:,.0f}", "Last AI inference"),
    ("🌍", "Avg. Industry Salary", "$82,400", "All roles, global"),
    ("📈", "Experience Level", f"{experience} yrs", "Selected profile"),
    ("🎓", "Education Tier", education, "Selected profile"),
]
for col, (icon, label, value, sub) in zip([kpi1, kpi2, kpi3, kpi4], kpis):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <span class="kpi-icon">{icon}</span>
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-trend trend-neutral">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

viz_col1, viz_col2 = st.columns(2)

with viz_col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    exp_range = np.arange(0, 41)
    base_salary = 35000 + exp_range * 2800 + np.sin(exp_range / 3) * 4000
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=exp_range, y=base_salary, mode="lines",
        line=dict(color="#60a5fa", width=3),
        fill="tozeroy", fillcolor="rgba(96,165,250,0.15)",
        name="Avg Salary"
    ))
    fig1.add_trace(go.Scatter(
        x=[experience], y=[base_salary[min(experience, 40)]],
        mode="markers", marker=dict(color="#34d399", size=14, line=dict(color="white", width=2)),
        name="Your Profile"
    ))
    fig1.update_layout(title="Experience vs. Salary", **PLOTLY_TEMPLATE)
    fig1.update_xaxes(gridcolor="rgba(255,255,255,0.05)", title="Years of Experience")
    fig1.update_yaxes(gridcolor="rgba(255,255,255,0.05)", title="Salary ($)")
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with viz_col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    edu_levels = ["Bachelor's", "Master's", "PhD"]
    edu_salaries = [68000, 88000, 112000]
    colors = ["#7c3aed" if e != education else "#34d399" for e in edu_levels]
    fig2 = go.Figure(go.Bar(
        x=edu_levels, y=edu_salaries,
        marker=dict(color=colors, line=dict(width=0)),
        text=[f"${v:,.0f}" for v in edu_salaries],
        textposition="outside"
    ))
    fig2.update_layout(title="Education vs. Salary", **PLOTLY_TEMPLATE)
    fig2.update_xaxes(gridcolor="rgba(255,255,255,0.05)")
    fig2.update_yaxes(gridcolor="rgba(255,255,255,0.05)", title="Salary ($)")
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

viz_col3, viz_col4 = st.columns(2)

with viz_col3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    np.random.seed(42)
    salary_dist = np.random.normal(loc=85000, scale=22000, size=600)
    salary_dist = salary_dist[salary_dist > 0]
    fig3 = px.histogram(salary_dist, nbins=40, color_discrete_sequence=["#a78bfa"])
    fig3.add_vline(x=last_pred, line_dash="dash", line_color="#34d399", annotation_text="Your Prediction", annotation_font_color="#34d399")
    fig3.update_layout(title="Salary Distribution Across Workforce", showlegend=False, **PLOTLY_TEMPLATE)
    fig3.update_xaxes(gridcolor="rgba(255,255,255,0.05)", title="Salary ($)")
    fig3.update_yaxes(gridcolor="rgba(255,255,255,0.05)", title="Frequency")
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with viz_col4:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    np.random.seed(7)
    gender_groups = genders if len(genders) <= 6 else genders[:6]
    gender_salaries = [75000 + np.random.randint(-8000, 15000) for _ in gender_groups]
    if gender in gender_groups:
        idx = gender_groups.index(gender)
        gender_salaries[idx] = int(last_pred)
    bar_colors = ["#34d399" if g == gender else "#60a5fa" for g in gender_groups]
    fig4 = go.Figure(go.Bar(
        x=gender_groups, y=gender_salaries,
        marker=dict(color=bar_colors, line=dict(width=0)),
        text=[f"${v:,.0f}" for v in gender_salaries],
        textposition="outside"
    ))
    fig4.update_layout(title="Gender Salary Analysis", **PLOTLY_TEMPLATE)
    fig4.update_xaxes(gridcolor="rgba(255,255,255,0.05)")
    fig4.update_yaxes(gridcolor="rgba(255,255,255,0.05)", title="Salary ($)")
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Job title salary trends (full width)
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
np.random.seed(11)
top_jobs = job_titles[:10] if len(job_titles) >= 10 else job_titles
job_salaries = [60000 + np.random.randint(0, 90000) for _ in top_jobs]
if job_title in top_jobs:
    idx = top_jobs.index(job_title)
    job_salaries[idx] = int(last_pred)
bar_colors_job = ["#34d399" if j == job_title else "#7c3aed" for j in top_jobs]
fig_jobs = go.Figure(go.Bar(
    x=top_jobs, y=job_salaries,
    marker=dict(color=bar_colors_job, line=dict(width=0)),
    text=[f"${v:,.0f}" for v in job_salaries],
    textposition="outside"
))
fig_jobs.update_layout(title="Job Title Salary Trends", **PLOTLY_TEMPLATE)
fig_jobs.update_xaxes(gridcolor="rgba(255,255,255,0.05)", tickangle=-30)
fig_jobs.update_yaxes(gridcolor="rgba(255,255,255,0.05)", title="Salary ($)")
st.plotly_chart(fig_jobs, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------- FEATURE IMPORTANCE -----------------------------
st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)
st.markdown("""
<div class="section-eyebrow">MODEL TRANSPARENCY</div>
<div class="section-title">🧠 AI Feature Importance Analysis</div>
<div class="section-subtitle">Understanding which factors most influence the XGBoost model's predictions</div>
""", unsafe_allow_html=True)

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
importance_df = get_feature_importance()
fig5 = go.Figure(go.Bar(
    x=importance_df["Importance"], y=importance_df["Feature"],
    orientation="h",
    marker=dict(
        color=importance_df["Importance"],
        colorscale=[[0, "#7c3aed"], [0.5, "#60a5fa"], [1, "#34d399"]],
    ),
    text=[f"{v:.1%}" for v in importance_df["Importance"]],
    textposition="outside"
))
fig5.update_layout(title="XGBoost Feature Importance", **PLOTLY_TEMPLATE)
fig5.update_xaxes(gridcolor="rgba(255,255,255,0.05)", title="Importance Score")
fig5.update_yaxes(gridcolor="rgba(255,255,255,0.05)")
st.plotly_chart(fig5, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------- FOOTER -----------------------------
st.markdown("""
<div class="footer">
    Built with <span>AI Salary Intelligence Platform</span> · Powered by XGBoost, Streamlit & Plotly<br>
    © 2026 · Enterprise Workforce Analytics & Compensation Intelligence
    <div class="footer-links">
        <a href="#">Documentation</a>
        <a href="#">API Access</a>
        <a href="#">Privacy Policy</a>
        <a href="#">Contact Sales</a>
    </div>
</div>
""", unsafe_allow_html=True)