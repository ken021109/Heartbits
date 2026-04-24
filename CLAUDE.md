# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

## Project Overview

**Stroke Alert VN** — A Vietnamese stroke risk screening web app for elderly users. It combines a Logistic Regression ML model (trained on the Kaggle Stroke Prediction Dataset) with real-time FAST symptom assessment to produce a 0–100 risk score with actionable recommendations.

## Tech Stack

- **Python 3.9+** (recommended 3.11)
- **Streamlit** — web UI framework
- **scikit-learn** — LogisticRegression (balanced), StandardScaler
- **pandas / numpy** — data processing
- **joblib** — model serialization

## Key Files

| File | Purpose |
|---|---|
| `app.py` | Main Streamlit application (~650 lines). Handles UI input, ML prediction, FAST scoring, hybrid risk calculation, XAI visualization, and hospital finder. |
| `training_logicstic.py` | Training pipeline. Reads CSV → preprocesses → trains LogisticRegression → exports `stroke_final_model.pkl` + `preprocessor_meta.pkl`. |
| `main.py` | Legacy prototype (rule-based scoring only, no ML). Kept for reference. |
| `healthcare-dataset-stroke-data.csv` | Kaggle stroke dataset (~5110 rows). |
| `stroke_final_model.pkl` | Trained model artifact. |
| `preprocessor_meta.pkl` | Scaler, median values, feature names, model coefficients. |
| `stroke_app.db` | SQLite DB exists but is currently unused. |

## Common Commands

### Setup (first time)
```
setup.bat
```
Creates `venv`, upgrades pip, installs dependencies from `requirements.txt`.

### Train / retrain model
```
train.bat
```
Runs `training_logicstic.py` inside venv. Requires `healthcare-dataset-stroke-data.csv` present. Outputs `stroke_final_model.pkl` and `preprocessor_meta.pkl`.

Or directly:
```
venv\Scripts\activate
python training_logicstic.py
```

### Run the app
```
run.bat
```
Or directly:
```
venv\Scripts\activate
streamlit run app.py
```

### Install / update dependencies
```
venv\Scripts\activate
pip install -r requirements.txt
```

## Architecture

### Hybrid Scoring System

The final risk score is a weighted combination:

```
final_score = (ml_score × 0.6) + (fast_score × 0.4) + bp_bonus
```

- **ml_score (60%)**: `predict_proba()` from the Logistic Regression model, scaled to 0–100. Uses features: age, hypertension, heart_disease, avg_glucose_level, bmi, plus one-hot encoded gender/work_type/smoking_status.
- **fast_score (40%)**: Rule-based from 4 FAST symptoms (Face, Arm, Speech, Headache), each rated 0–3. Formula: `(F² + A² + S² + T²) × 8.5`, capped at 100.
- **bp_bonus**: If blood pressure is measured, adds up to +20 points based on systolic overrun above 115 mmHg.

### Safety Overrides

- FAST max level = 3 ("Nặng") → score forced to 99, emergency alert shown.
- FAST max level = 2 ("Rõ") → score floored at 80.

These overrides take priority over the ML prediction, prioritizing patient safety.

### Explainable AI (XAI)

Feature contribution is calculated as `|coefficient × scaled_value|` from the Logistic Regression model, grouped into 7 categories: Tuổi tác, Huyết áp/Tim, Đường huyết, BMI, Hút thuốc, Nghề nghiệp, Giới tính. FAST symptoms are shown separately.

### Data Flow

```
User Input (app.py)
  → build_row() → DataFrame with one-hot encoded features matching training schema
  → StandardScaler.transform() on numerical cols
  → model.predict_proba() → ml_score
  → calc_fast_pts() → fast_score
  → combine + bp_bonus + safety overrides → final_score
  → render result + XAI breakdown + hospital search link
```

### Training Pipeline (`training_logicstic.py`)

1. Load CSV, drop `id`, `ever_married`, `Residence_type`
2. Fill missing BMI/glucose with median
3. One-hot encode: `gender`, `work_type`, `smoking_status`
4. Train/test split (80/20, stratified)
5. StandardScaler on `age`, `avg_glucose_level`, `bmi`
6. LogisticRegression(max_iter=3000, class_weight="balanced")
7. Export model + preprocessor metadata via joblib

### UI Design Notes

- All labels and messages are in Vietnamese.
- Font: Lexend (loaded from Google Fonts). Large font sizes for elderly accessibility.
- High contrast mode available in sidebar.
- No authentication, no user accounts, no data persistence (stateless per session).
