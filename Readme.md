💰 AI Salary Prediction System

An end-to-end Machine Learning project that predicts employee salaries using demographic, educational, and professional attributes with the power of XGBoost Regression.

📌 Overview

Salary estimation plays a crucial role in workforce planning, compensation analysis, and career decision-making. This project leverages Machine Learning to predict employee salaries based on key factors such as age, education level, job title, and years of experience.

The model is trained using XGBoost Regressor and achieves an impressive R² Score of 0.9378, demonstrating strong predictive performance.

🚀 Features
Data Cleaning & Preprocessing
Missing Value Handling
Label Encoding & One-Hot Encoding
Feature Engineering
XGBoost Regression Model
Model Evaluation using Multiple Metrics
Interactive Streamlit Web Application
Real-Time Salary Prediction
Professional Dashboard Interface
📊 Dataset Information

The dataset contains employee-related information used for salary prediction.

Feature	Description
Age	Employee Age
Gender	Male / Female
Job Title	Employee Designation
Years of Experience	Professional Experience
Education Level	Bachelor's, Master's, PhD
Salary	Target Variable
🛠️ Tech Stack
Programming Language
Python
Libraries & Frameworks
Pandas
NumPy
Scikit-Learn
XGBoost
Joblib
Streamlit
Plotly
⚙️ Data Preprocessing
Handling Missing Values
Column	Strategy
Age	Mean Imputation
Years of Experience	Mean Imputation
Salary	Mean Imputation
Gender	Mode Imputation
Job Title	Mode Imputation
Education Level	Mode Imputation
Encoding Techniques
Label Encoding

Applied to:

Gender
Job Title
One-Hot Encoding

Applied to:

Education Level

Generated Features:

Education Level_Bachelor's
Education Level_Master's
Education Level_PhD
🤖 Machine Learning Model
XGBoost Regressor
model = XGBRegressor(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    random_state=43
)
Train-Test Split
train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=43
)
📈 Model Performance

The model was evaluated using standard regression metrics.

Metric	Value
R² Score	0.9378
Mean Absolute Error (MAE)	Evaluated
Mean Squared Error (MSE)	Evaluated
Interpretation

An R² Score of 0.9378 indicates that the model successfully explains approximately 93.78% of the variance in salary, making it a highly effective regression model for this dataset.

📂 Project Structure
Salary_Prediction/
│
├── app.py
├── SalaryPrediction.ipynb
├── Salary Data.csv
├── salary_prediction_model.pkl
├── gender_encoder.pkl
├── job_title_encoder.pkl
├── requirements.txt
└── README.md