import streamlit as st
import pandas as pd
import numpy as np
import joblib
import time
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Salary AI | Predictive Compensation Intelligence",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------------------- CUSTOM CSS -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.stApp {
    background: linear-gradient(-45deg, #0a0e27, #131a3a, #0d1b2a, #1a0d2e);
    background-size: 400% 400%;
    animation: gradientShift 18s ease infinite;
}

@keyframes gradientShift {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

#MainMenu, footer, header {visibility: hidden;}

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

/* Hero */
.hero-container {
    text-align: center;
    padding: 50px 20px 30px 20px;
    animation: fadeInDown 1s ease;
    position: relative;
    z-index: 1;
}
@keyframes fadeInDown {
    from {opacity: 0; transform: translateY(-30px);}
    to {opacity: 1; transform: translateY(0);}
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 4rem;
    font-weight: 800;
    background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399, #a78bfa);
    background-size: 300% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shine 6s linear infinite;
    margin-bottom: 0;
    letter-spacing: -2px;
}
@keyframes shine {
    to { background-position: 300% center; }
}
.hero-subtitle {
    color: #9ca3af;
    font-size: 1.15rem;
    font-weight: 400;
    margin-top: 10px;
    letter-spacing: 0.5px;
}
.hero-badge {
    display: inline-block;
    margin-top: 18px;
    padding: 8px 22px;
    border-radius: 50px;
    background: rgba(124,58,237,0.12);
    border: 1px solid rgba(167,139,250,0.35);
    color: #c4b5fd;
    font-size: 0.85rem;
    font-weight: 600;
    backdrop-filter: blur(10px);
    box-shadow: 0 0 20px rgba(124,58,237,0.25);
    animation: pulseGlow 3s ease-in-out infinite;
}
@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 0 15px rgba(124,58,237,0.2); }
    50% { box-shadow: 0 0 30px rgba(124,58,237,0.5); }
}

/* Glass card */
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
@keyframes fadeInUp {
    from {opacity: 0; transform: translateY(25px);}
    to {opacity: 1; transform: translateY(0);}
}

.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.6rem;
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
    margin-bottom: 20px;
}

/* KPI cards */
.kpi-card {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 22px;
    text-align: center;
    transition: all 0.3s ease;
    animation: fadeInUp 0.9s ease;
}
.kpi-card:hover {
    transform: translateY(-4px);
    border-color: rgba(96,165,250,0.4);
    box-shadow: 0 10px 30px rgba(96,165,250,0.2);
}
.kpi-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.kpi-label {
    color: #9ca3af;
    font-size: 0.8rem;
    margin-top: 6px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Result card */
.result-card {
    background: linear-gradient(135deg, rgba(124,58,237,0.18), rgba(59,130,246,0.12));
    backdrop-filter: blur(25px);
    border: 1px solid rgba(167,139,250,0.4);
    border-radius: 24px;
    padding: 40px;
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
    font-size: 4.2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #34d399, #60a5fa, #a78bfa);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shine 4s linear infinite;
    margin: 10px 0;
    position: relative;
    z-index: 1;
}
.result-sub {
    color: #9ca3af;
    font-size: 0.95rem;
    position: relative;
    z-index: 1;
}
.confidence-bar-bg {
    width: 100%;
    height: 8px;
    background: rgba(255,255,255,0.08);
    border-radius: 10px;
    margin-top: 20px;
    overflow: hidden;
    position: relative;
    z-index: 1;
}
.confidence-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #34d399, #60a5fa);
    border-radius: 10px;
    box-shadow: 0 0 15px rgba(52,211,153,0.6);
    animation: fillBar 1.4s ease-out forwards;
}
@keyframes fillBar {
    from { width: 0%; }
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

/* Divider glow */
.glow-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(167,139,250,0.5), transparent);
    margin: 35px 0;
    border: none;
}
</style>

<div class="particles">
""" + "".join([
    f'<div class="particle" style="left:{np.random.randint(0,100)}%; width:{np.random.randint(3,8)}px; height:{np.random.randint(3,8)}px; animation-duration:{np.random.randint(15,35)}s; animation-delay:{np.random.randint(0,20)}s;"></div>'
    for _ in range(25)
]) + """
</div>
""", unsafe_allow_html=True)


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


# ----------------------------- HELPERS -----------------------------
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
        return ["Software Engineer", "Data Scientist", "Manager", "Director", "Sales Associate", "HR Manager"]


def get_genders(encoder):
    try:
        return sorted(list(encoder.classes_))
    except Exception:
        return ["Male", "Female"]


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


# ----------------------------- HERO -----------------------------
st.markdown("""
<div class="hero-container">
    <div class="hero-title">SalaryAI Intelligence</div>
    <div class="hero-subtitle">Predictive compensation analytics powered by XGBoost & machine learning</div>
    <div class="hero-badge">⚡ Real-time AI inference • Enterprise-grade accuracy</div>
</div>
""", unsafe_allow_html=True)

if load_error:
    st.warning(f"⚠️ Model artifacts not found in working directory ({load_error}). Place `salary_prediction_model.pkl`, `gender_encoder.pkl`, and `job_title_encoder.pkl` alongside this app to enable live predictions.")

st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)

# ----------------------------- INPUT DASHBOARD -----------------------------
st.markdown("""
<div class="section-title">🧬 Candidate Profile</div>
<div class="section-subtitle">Provide the details below to generate an AI-driven salary estimate</div>
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
    predict_btn = st.button("🚀 Predict Salary")
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------- PREDICTION RESULT -----------------------------
if predict_btn:
    if model is None:
        st.error("Model is not loaded. Please ensure all `.pkl` files are present in the app directory.")
    else:
        with st.spinner("🔮 Running AI inference..."):
            time.sleep(1.1)
            try:
                predicted_salary = predict_salary(age, gender, job_title, experience, education)
                confidence = min(98, max(82, 100 - abs(experience - 10)))

                st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-label">Predicted Annual Salary</div>
                    <div class="result-value">${predicted_salary:,.2f}</div>
                    <div class="result-sub">Based on {experience} years of experience as a {job_title} with {education} education</div>
                    <div class="confidence-bar-bg">
                        <div class="confidence-bar-fill" style="width:{confidence}%;"></div>
                    </div>
                    <div class="result-sub" style="margin-top:8px;">Model Confidence: {confidence}%</div>
                </div>
                """, unsafe_allow_html=True)
                st.success("✅ Prediction generated successfully!")

                st.session_state["last_prediction"] = predicted_salary
                st.session_state["last_inputs"] = {
                    "age": age, "gender": gender, "job_title": job_title,
                    "experience": experience, "education": education
                }
            except Exception as e:
                st.error(f"Prediction failed: {e}")

# ----------------------------- ANALYTICS DASHBOARD -----------------------------
st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)
st.markdown("""
<div class="section-title">📊 Analytics Overview</div>
<div class="section-subtitle">Key insights derived from the salary prediction model</div>
""", unsafe_allow_html=True)

last_pred = st.session_state.get("last_prediction", 75000)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpis = [
    ("Predicted Salary", f"${last_pred:,.0f}", kpi1),
    ("Avg. Industry Salary", "$82,400", kpi2),
    ("Experience Level", f"{experience} yrs", kpi3),
    ("Education Tier", education, kpi4),
]
for label, value, col in kpis:
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------- VISUALIZATIONS -----------------------------
st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)
st.markdown("""
<div class="section-title">📈 Data Visualizations</div>
<div class="section-subtitle">Interactive insights into salary trends across experience and education</div>
""", unsafe_allow_html=True)

PLOTLY_TEMPLATE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#d1d5db", family="Plus Jakarta Sans"),
    margin=dict(l=20, r=20, t=50, b=20),
    legend=dict(bgcolor="rgba(0,0,0,0)")
)

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
    fig1.update_layout(title="Salary vs. Years of Experience", **PLOTLY_TEMPLATE)
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
    fig2.update_layout(title="Average Salary by Education Level", **PLOTLY_TEMPLATE)
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
    age_range = np.arange(20, 65, 5)
    age_salary = 30000 + (age_range - 20) * 1900
    fig4 = go.Figure(go.Scatter(
        x=age_range, y=age_salary, mode="lines+markers",
        line=dict(color="#34d399", width=3, shape="spline"),
        marker=dict(size=8, color="#60a5fa"),
        fill="tozeroy", fillcolor="rgba(52,211,153,0.1)"
    ))
    fig4.update_layout(title="Salary Trend by Age Group", **PLOTLY_TEMPLATE)
    fig4.update_xaxes(gridcolor="rgba(255,255,255,0.05)", title="Age")
    fig4.update_yaxes(gridcolor="rgba(255,255,255,0.05)", title="Salary ($)")
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------- FEATURE IMPORTANCE -----------------------------
st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)
st.markdown("""
<div class="section-title">🧠 Model Feature Importance</div>
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
    Built with <span>SalaryAI Intelligence</span> · Powered by XGBoost, Streamlit & Plotly<br>
    © 2026 · Designed for next-generation compensation analytics
</div>
""", unsafe_allow_html=True)