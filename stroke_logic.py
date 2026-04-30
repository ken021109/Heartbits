import os
from typing import Dict, Iterable, Tuple

import pandas as pd

FAST_SEVERE_THRESHOLD = 15
FAST_CLEAR_THRESHOLD = 10


def load_artifacts(
    model_path: str = "stroke_final_model.pkl",
    meta_path: str = "preprocessor_meta.pkl",
):
    import joblib

    if not os.path.exists(model_path) or not os.path.exists(meta_path):
        return None, None

    return joblib.load(model_path), joblib.load(meta_path)


def build_feature_row(
    age,
    gender,
    work_type,
    smoking_status,
    hypertension,
    heart_disease,
    avg_glucose_level,
    bmi,
    feature_names: Iterable[str],
) -> pd.DataFrame:
    row = {
        "age": float(age),
        "hypertension": int(hypertension),
        "heart_disease": int(heart_disease),
        "avg_glucose_level": float(avg_glucose_level),
        "bmi": float(bmi),
    }

    category_values = {
        "gender_": gender,
        "work_type_": work_type,
        "smoking_status_": smoking_status,
    }

    for feature_name in feature_names:
        for prefix, selected_value in category_values.items():
            if feature_name.startswith(prefix):
                row[feature_name] = int(feature_name[len(prefix):] == selected_value)
                break

    df = pd.DataFrame([row])
    for feature_name in feature_names:
        if feature_name not in df.columns:
            df[feature_name] = 0

    return df[list(feature_names)]


def get_ml_probability(df_row: pd.DataFrame, scaler, model) -> float:
    df_scaled = df_row.copy()
    scaled_cols = ["age", "avg_glucose_level", "bmi"]
    df_scaled[scaled_cols] = scaler.transform(df_row[scaled_cols])
    return float(model.predict_proba(df_scaled)[0][1])


def calc_fast_points(*values: int) -> int:
    return sum(values)


def compute_risk_summary(ml_probability: float, fast_values: Dict[str, int]) -> Dict[str, object]:
    ml_score = int(ml_probability * 100)
    fast_sum = calc_fast_points(*fast_values.values())
    combined_score = int(ml_score * 0.4 + fast_sum)
    final_score = min(99, combined_score)
    override_msg = None

    max_fast_value = max(fast_values.values()) if fast_values else 0
    clear_or_higher_count = sum(
        1 for value in fast_values.values() if value >= FAST_CLEAR_THRESHOLD
    )

    if max_fast_value == FAST_SEVERE_THRESHOLD:
        final_score = 99
        override_msg = (
            "CẢNH BÁO: Triệu chứng FAST ở mức NẶNG — tình trạng CỰC KỲ KHẨN CẤP.\n"
            "GỌI CẤP CỨU 115 NGAY LẬP TỨC!"
        )
    elif clear_or_higher_count >= 2 and final_score < 80:
        final_score = 80
        override_msg = (
            "Lưu ý: Có ít nhất 2 triệu chứng FAST ở mức RÕ hoặc cao hơn — "
            "điểm nguy cơ được điều chỉnh lên tối thiểu 80/100 để đảm bảo an toàn."
        )

    return {
        "ml_score": ml_score,
        "fast_sum": fast_sum,
        "combined_score": combined_score,
        "final_score": final_score,
        "override_msg": override_msg,
    }


def calc_xai_groups(df_row: pd.DataFrame, meta) -> Dict[str, float]:
    coeffs = meta["model_coefficients"]
    scaler = meta["scaler"]
    feature_names = meta["feature_names"]
    df_scaled = df_row.copy()
    scaled_cols = ["age", "avg_glucose_level", "bmi"]
    df_scaled[scaled_cols] = scaler.transform(df_row[scaled_cols])

    groups = {
        "Tuổi tác": ["age"],
        "Huyết áp / Tim": ["hypertension", "heart_disease"],
        "Đường huyết": ["avg_glucose_level"],
        "Chỉ số BMI": ["bmi"],
        "Hút thuốc": [name for name in feature_names if name.startswith("smoking_status_")],
        "Nghề nghiệp": [name for name in feature_names if name.startswith("work_type_")],
        "Giới tính": [name for name in feature_names if name.startswith("gender_")],
    }

    return {
        group_name: round(
            sum(abs(coeffs.get(col_name, 0) * df_scaled[col_name].values[0]) for col_name in cols),
            3,
        )
        for group_name, cols in groups.items()
    }


def get_score_meta(score: int) -> Tuple[str, str, str]:
    if score >= 70:
        return "#C0392B", "NGUY CƠ RẤT CAO", "error"
    if score >= 50:
        return "#D85A30", "NGUY CƠ CAO", "error"
    if score >= 30:
        return "#D4A017", "NGUY CƠ TRUNG BÌNH", "warning"
    return "#27AE60", "NGUY CƠ THẤP", "success"
