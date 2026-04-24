"""
train_model.py — Stroke Alert VN
Chạy script này TRƯỚC khi chạy app.py.
Yêu cầu: file 'healthcare-dataset-stroke-data.csv' cùng thư mục.
Output: stroke_final_model.pkl và preprocessor_meta.pkl
"""

import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, recall_score

print("=" * 50)
print("  STROKE ALERT VN — TRAINING PIPELINE V2")
print("=" * 50)

# ──────────────────────────────────────────────
# 1. ĐỌC VÀ LÀM SẠCH DỮ LIỆU
# ──────────────────────────────────────────────
try:
    raw_data = pd.read_csv("healthcare-dataset-stroke-data.csv")
    print(f"\n✅ Đã nạp dữ liệu: {len(raw_data):,} hàng, {raw_data.shape[1]} cột.")
except FileNotFoundError:
    print("\n❌ LỖI: Không tìm thấy 'healthcare-dataset-stroke-data.csv'.")
    print("   Tải tại: https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset")
    exit(1)

# Loại bỏ cột không cần thiết (V2: bỏ ever_married và Residence_type)
cols_to_drop = ["id", "ever_married", "Residence_type"]
stroke_df = raw_data.drop(columns=cols_to_drop)

# ──────────────────────────────────────────────
# 2. XỬ LÝ GIÁ TRỊ THIẾU (NO-NA STRATEGY)
# ──────────────────────────────────────────────
median_bmi_val     = stroke_df["bmi"].median()
median_glucose_val = stroke_df["avg_glucose_level"].median()

stroke_df["bmi"] = stroke_df["bmi"].fillna(median_bmi_val)
# Glucose thường đủ trong dataset gốc; median được lưu để App dùng làm default

print(f"   Median BMI    : {median_bmi_val:.2f}")
print(f"   Median Glucose: {median_glucose_val:.2f}")

# ──────────────────────────────────────────────
# 3. ONE-HOT ENCODING
# ──────────────────────────────────────────────
categorical_features = ["gender", "work_type", "smoking_status"]
stroke_df_encoded = pd.get_dummies(stroke_df, columns=categorical_features)

# ──────────────────────────────────────────────
# 4. CHUẨN BỊ X / y
# ──────────────────────────────────────────────
X = stroke_df_encoded.drop(columns=["stroke"])
y = stroke_df_encoded["stroke"]

print(f"\n   Features      : {X.shape[1]} cột")
print(f"   Stroke cases  : {y.sum()} / {len(y)} ({y.mean()*100:.1f}%)")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ──────────────────────────────────────────────
# 5. CHUẨN HÓA (StandardScaler — chỉ fit trên Train)
# ──────────────────────────────────────────────
numerical_cols = ["age", "avg_glucose_level", "bmi"]
scaler = StandardScaler()

X_train = X_train.copy()
X_test  = X_test.copy()
X_train[numerical_cols] = scaler.fit_transform(X_train[numerical_cols])
X_test[numerical_cols]  = scaler.transform(X_test[numerical_cols])

# ──────────────────────────────────────────────
# 6. HUẤN LUYỆN (Logistic Regression balanced)
# ──────────────────────────────────────────────
final_model = LogisticRegression(
    max_iter=3000,
    class_weight="balanced",
    random_state=42,
)
final_model.fit(X_train, y_train)

# ──────────────────────────────────────────────
# 7. ĐÁNH GIÁ
# ──────────────────────────────────────────────
y_pred = final_model.predict(X_test)
acc    = final_model.score(X_test, y_test)
rec    = recall_score(y_test, y_pred)

print("\n" + "=" * 50)
print("  KẾT QUẢ ĐÁNH GIÁ MÔ HÌNH V2")
print("=" * 50)
print(f"  Accuracy : {acc:.2f}")
print(f"  Recall   : {rec:.2f}   (Mục tiêu: 0.75 – 0.85)")
print("-" * 50)
print(classification_report(y_test, y_pred, target_names=["Không đột quỵ", "Đột quỵ"]))
print("=" * 50)

# ──────────────────────────────────────────────
# 8. ĐÓNG GÓI ARTIFACTS
# ──────────────────────────────────────────────
preprocessor_meta = {
    "scaler"             : scaler,
    "median_bmi"         : median_bmi_val,
    "median_glucose"     : median_glucose_val,
    "feature_names"      : X.columns.tolist(),
    "model_coefficients" : dict(zip(X.columns, final_model.coef_[0])),
}

joblib.dump(final_model,      "stroke_final_model.pkl")
joblib.dump(preprocessor_meta, "preprocessor_meta.pkl")

print("\n✅ Đã xuất:")
print("   • stroke_final_model.pkl")
print("   • preprocessor_meta.pkl")
print("\n🚀 Sẵn sàng chạy app:  streamlit run app.py")