"""
app.py — Stroke Alert VN  v3
Chạy: streamlit run app.py
"""

import os
from datetime import datetime

import joblib
import numpy as np
import pandas as pd
import streamlit as st

# ╔══════════════════════════════════════════════════════════════════════╗
# ║  0. PAGE CONFIG                                                      ║
# ╚══════════════════════════════════════════════════════════════════════╝

st.set_page_config(
    page_title="Stroke Alert VN",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ╔══════════════════════════════════════════════════════════════════════╗
# ║  1. GLOBAL CSS                                                       ║
# ╚══════════════════════════════════════════════════════════════════════╝

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lexend:wght@400;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Lexend', sans-serif !important; }

h1  { font-size: 2.2rem  !important; font-weight: 800 !important; line-height: 1.2 !important; }
h2  { font-size: 1.75rem !important; font-weight: 700 !important; }
h3  { font-size: 1.4rem  !important; font-weight: 700 !important; }
p, li, label, .stMarkdown p { font-size: 1.15rem !important; line-height: 1.75 !important; }

.stRadio     > label,
.stCheckbox  > label,
.stSelectbox > label,
.stNumberInput > label,
.stSlider    > label,
.stTextInput > label { font-size: 1.15rem !important; font-weight: 700 !important; }

.stNumberInput input,
.stTextInput  input  { font-size: 1.25rem !important; font-weight: 600 !important;
                        padding: 0.55rem 0.85rem !important; }

div[data-baseweb="select"] > div { font-size: 1.1rem !important; }

.stRadio    div[data-testid="stMarkdownContainer"] p,
.stCheckbox div[data-testid="stMarkdownContainer"] p { font-size: 1.1rem !important; font-weight: 600 !important; }

.stButton > button {
    font-size: 1.3rem  !important;
    font-weight: 800   !important;
    padding: 0.75rem 1.5rem !important;
    border-radius: 12px !important;
    width: 100% !important;
}
.stLinkButton > a {
    font-size: 1.1rem !important; font-weight: 700 !important;
    display: block !important; text-align: center !important;
    padding: 0.7rem 1rem !important; border-radius: 12px !important;
}

.card-title {
    font-size: 1.05rem; font-weight: 800; letter-spacing: .05em;
    text-transform: uppercase; color: #1a2744;
    border-left: 5px solid #1a2744; padding-left: .65rem;
    margin-bottom: 1.1rem;
}

.score-wrap { background:#e9ecef; border-radius:12px; height:30px; overflow:hidden; margin:.5rem 0 1rem; }
.score-fill { height:100%; border-radius:12px; display:flex; align-items:center;
              justify-content:flex-end; padding-right:12px;
              font-weight:800; font-size:1rem; color:#fff; }

.xai-outer { background:#e9ecef; border-radius:6px; height:18px; overflow:hidden; }
.xai-inner { height:100%; border-radius:6px; }

.override-box {
    background:#4A1B0C; color:#F0997B; border-radius:12px;
    padding:1rem 1.2rem; font-size:1.1rem; font-weight:700;
    line-height:1.65; margin-top:.75rem;
}

.pill { display:inline-block; border-radius:20px; padding:.2rem .75rem;
        font-size:.95rem; font-weight:700; }
.pill-green  { background:#EAF3DE; color:#3B6D11; }
.pill-yellow { background:#FAEEDA; color:#854F0B; }
.pill-orange { background:#FAECE7; color:#993C1D; }
.pill-red    { background:#FCEBEB; color:#A32D2D; }

hr { margin: 1.5rem 0 !important; border-color: #dee2e6 !important; }
</style>
""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════════╗
# ║  2. LOAD ARTIFACTS                                                   ║
# ╚══════════════════════════════════════════════════════════════════════╝

@st.cache_resource(show_spinner="Đang nạp mô hình AI...")
def load_artifacts():
    if not os.path.exists("stroke_final_model.pkl"):
        return None, None
    return (
        joblib.load("stroke_final_model.pkl"),
        joblib.load("preprocessor_meta.pkl"),
    )

model, meta = load_artifacts()


# ╔══════════════════════════════════════════════════════════════════════╗
# ║  3. CONSTANTS & HELPERS                                              ║
# ╚══════════════════════════════════════════════════════════════════════╝

FAST_OPTS = ["Không", "Nhẹ", "Rõ", "Nặng"]
FAST_INT  = {"Không": 0, "Nhẹ": 1, "Rõ": 2, "Nặng": 3}
FAST_PILL = {"Không": "pill-green", "Nhẹ": "pill-yellow", "Rõ": "pill-orange", "Nặng": "pill-red"}
NOW_YEAR  = datetime.now().year

XAI_COLORS = {
    "Tuổi tác"      : "#378ADD",
    "Huyết áp / Tim": "#E24B4A",
    "Đường huyết"   : "#EF9F27",
    "Chỉ số BMI"    : "#5DCAA5",
    "Hút thuốc"     : "#D85A30",
    "Nghề nghiệp"   : "#888780",
    "Giới tính"     : "#9B59B6",
}


def card(title: str):
    st.markdown(f'<div class="card-title">{title}</div>', unsafe_allow_html=True)


def pill_html(text: str, cls: str) -> str:
    return f'<span class="pill {cls}">{text}</span>'


def build_row(age, gender, work_type, smoking_status,
              hypertension, heart_disease,
              avg_glucose_level, bmi, feature_names) -> pd.DataFrame:
    row = {
        "age"              : float(age),
        "hypertension"     : int(hypertension),
        "heart_disease"    : int(heart_disease),
        "avg_glucose_level": float(avg_glucose_level),
        "bmi"              : float(bmi),
        "gender_Female"          : int(gender == "Female"),
        "gender_Male"            : int(gender == "Male"),
        "gender_Other"           : int(gender == "Other"),
        "work_type_Govt_job"     : int(work_type == "Govt_job"),
        "work_type_Never_worked" : int(work_type == "Never_worked"),
        "work_type_Private"      : int(work_type == "Private"),
        "work_type_Self-employed": int(work_type == "Self-employed"),
        "work_type_children"     : int(work_type == "children"),
        "smoking_status_Unknown"        : int(smoking_status == "Unknown"),
        "smoking_status_formerly smoked": int(smoking_status == "formerly smoked"),
        "smoking_status_never smoked"   : int(smoking_status == "never smoked"),
        "smoking_status_smokes"         : int(smoking_status == "smokes"),
    }
    df = pd.DataFrame([row])
    for col in feature_names:
        if col not in df.columns:
            df[col] = 0
    return df[feature_names]


def get_ml_proba(df_row, scaler, mdl) -> float:
    df_s = df_row.copy()
    df_s[["age", "avg_glucose_level", "bmi"]] = scaler.transform(
        df_row[["age", "avg_glucose_level", "bmi"]]
    )
    return float(mdl.predict_proba(df_s)[0][1])


def calc_fast_pts(f, a, s, h) -> int:
    return min(100, int((f**2 + a**2 + s**2 + h**2) * 8.5))


def calc_xai_groups(df_row, meta) -> dict:
    coeffs = meta["model_coefficients"]
    scaler = meta["scaler"]
    feat   = meta["feature_names"]
    df_s   = df_row.copy()
    df_s[["age", "avg_glucose_level", "bmi"]] = scaler.transform(
        df_row[["age", "avg_glucose_level", "bmi"]]
    )
    groups = {
        "Tuổi tác"      : ["age"],
        "Huyết áp / Tim": ["hypertension", "heart_disease"],
        "Đường huyết"   : ["avg_glucose_level"],
        "Chỉ số BMI"    : ["bmi"],
        "Hút thuốc"     : [c for c in feat if c.startswith("smoking_status_")],
        "Nghề nghiệp"   : [c for c in feat if c.startswith("work_type_")],
        "Giới tính"     : [c for c in feat if c.startswith("gender_")],
    }
    return {
        name: round(
            sum(abs(coeffs.get(c, 0) * df_s[c].values[0]) for c in cols), 3
        )
        for name, cols in groups.items()
    }


def get_score_meta(score: int):
    if score >= 70: return "#C0392B", "NGUY CƠ RẤT CAO",    "error"
    if score >= 50: return "#D85A30", "NGUY CƠ CAO",         "error"
    if score >= 30: return "#D4A017", "NGUY CƠ TRUNG BÌNH", "warning"
    return              "#27AE60", "NGUY CƠ THẤP",           "success"


def render_score_bar(score: int, color: str):
    st.markdown(
        f'<div class="score-wrap">'
        f'<div class="score-fill" style="width:{score}%;background:{color};">'
        f'{score} / 100</div></div>',
        unsafe_allow_html=True,
    )


def render_xai_row(name: str, val: float, max_v: float, color: str):
    pct = int(val / max_v * 100) if max_v else 0
    c1, c2, c3 = st.columns([3, 6, 2])
    c1.markdown(f"**{name}**")
    c2.markdown(
        f'<div class="xai-outer">'
        f'<div class="xai-inner" style="width:{pct}%;background:{color};"></div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    c3.markdown(f"`{val:.2f}`")


# ╔══════════════════════════════════════════════════════════════════════╗
# ║  4. HEADER                                                           ║
# ╚══════════════════════════════════════════════════════════════════════╝

st.title("🧠 Stroke Alert VN")
st.markdown(
    "Công cụ **sàng lọc nguy cơ đột quỵ** — "
    "điền thông tin bên dưới rồi bấm **Kiểm tra** ở cuối trang."
)

if model is None:
    st.error(
        "**Chưa tìm thấy file model.**  \n"
        "Chạy `python train_model.py` trước để tạo `stroke_final_model.pkl`.",
        icon="⚠️",
    )
    st.stop()

st.divider()

# ╔══════════════════════════════════════════════════════════════════════╗
# ║  5. PHẦN A — THÔNG TIN CÁ NHÂN                                      ║
# ╚══════════════════════════════════════════════════════════════════════╝

with st.container(border=True):
    card("A  —  Thông tin cá nhân")

    c_ns, c_age = st.columns([3, 2])
    with c_ns:
        nam_sinh = st.number_input(
            "Năm sinh",
            min_value=1920, max_value=NOW_YEAR - 1,
            value=1960, step=1,
        )
    tuoi = NOW_YEAR - int(nam_sinh)
    with c_age:
        st.markdown("<br>", unsafe_allow_html=True)
        st.metric(label="Tuổi", value=str(tuoi))

    gt_lbl = st.radio("Giới tính", ["Nam", "Nữ", "Khác"], horizontal=True)
    gender  = {"Nam": "Male", "Nữ": "Female", "Khác": "Other"}[gt_lbl]

    work_opts = {
        "Nhân viên / Công nhân" : "Private",
        "Tự kinh doanh"         : "Self-employed",
        "Cán bộ / Công chức"    : "Govt_job",
        "Trẻ em (dưới 18 tuổi)" : "children",
        "Chưa từng đi làm"      : "Never_worked",
    }
    work_type = work_opts[st.selectbox("Nghề nghiệp", list(work_opts.keys()))]

    smoke_opts = {
        "Chưa bao giờ hút" : "never smoked",
        "Đã bỏ thuốc"      : "formerly smoked",
        "Đang hút"         : "smokes",
        "Không rõ"         : "Unknown",
    }
    smoking_status = smoke_opts[st.selectbox("Tình trạng hút thuốc", list(smoke_opts.keys()))]


# ╔══════════════════════════════════════════════════════════════════════╗
# ║  6. PHẦN B — CHỈ SỐ SỨC KHỎE                                        ║
# ╚══════════════════════════════════════════════════════════════════════╝

with st.container(border=True):
    card("B  —  Chỉ số sức khỏe")

    # ── Huyết áp ─────────────────────────────────
    st.markdown("**Huyết áp**")
    co_may = st.toggle("Tôi vừa đo huyết áp và có kết quả", value=True)

    ha_sys = None
    if co_may:
        with st.expander("Hướng dẫn đọc số đo", expanded=False):
            st.markdown(
                "- Nghỉ ngơi 5 phút trước khi đo  \n"
                "- Ngồi thẳng, tay đặt ngang tim  \n"
                "- **Số TRÊN** = Tâm thu (SYS)  \n"
                "- **Số DƯỚI** = Tâm trương (DIA)"
            )
        c1, c2 = st.columns(2)
        with c1:
            ha_sys = st.number_input("Số TRÊN — Tâm thu (mmHg)", 80, 260, 120, step=1)
        with c2:
            st.number_input("Số DƯỚI — Tâm trương (mmHg)", 40, 160, 80, step=1)
        if ha_sys >= 140:
            st.warning(
                f"Huyết áp tâm thu {ha_sys} mmHg — cao hơn ngưỡng bình thường (≥ 140 mmHg).",
                icon="⚠️",
            )
    else:
        st.info("Thông tin bệnh nền bên dưới sẽ được dùng để đánh giá thay thế.", icon="ℹ️")

    st.divider()

    # ── Đường huyết ──────────────────────────────
    st.markdown("**Đường huyết**")
    co_glucose = st.toggle("Tôi biết chỉ số đường huyết", value=False)
    if co_glucose:
        avg_glucose = float(st.number_input(
            "Đường huyết (mg/dL)",
            min_value=50.0, max_value=500.0, value=100.0, step=1.0,
            help="Lấy từ kết quả xét nghiệm gần nhất.",
        ))
        if avg_glucose > 200:
            st.warning("Đường huyết cao — có thể liên quan đến tiểu đường type 2.", icon="⚠️")
    else:
        avg_glucose = meta["median_glucose"]
        st.caption(
            f"Dùng giá trị trung vị từ tập dữ liệu y tế: **{avg_glucose:.1f} mg/dL**"
        )

    st.divider()

    # ── BMI ──────────────────────────────────────
    st.markdown("**Chỉ số BMI**")
    bmi_mode = st.radio(
        "Nhập BMI theo cách nào?",
        ["Không biết — dùng giá trị mặc định", "Nhập BMI trực tiếp", "Tính từ chiều cao & cân nặng"],
    )
    if bmi_mode == "Nhập BMI trực tiếp":
        bmi = float(st.number_input("BMI", 10.0, 65.0, 22.0, step=0.1))
    elif bmi_mode == "Tính từ chiều cao & cân nặng":
        c_h, c_w = st.columns(2)
        with c_h:
            h_cm = st.number_input("Chiều cao (cm)", 100, 220, 165, step=1)
        with c_w:
            w_kg = st.number_input("Cân nặng (kg)", 30, 200, 60, step=1)
        bmi = round(w_kg / (h_cm / 100) ** 2, 1)
        st.info(f"BMI tính được: **{bmi}**", icon="📐")
    else:
        bmi = meta["median_bmi"]
        st.caption(f"Dùng giá trị trung vị từ tập dữ liệu y tế: **{bmi:.1f}**")

    st.divider()

    # ── Bệnh nền — CHỈ 2 CÁI CÓ TRONG DATASET ───
    st.markdown(
        "**Bệnh nền** *(chỉ chọn những bệnh bác sĩ đã chính thức chẩn đoán)*"
    )
    c_b1, c_b2 = st.columns(2)
    with c_b1:
        hypertension  = st.checkbox("Cao huyết áp")
    with c_b2:
        heart_disease = st.checkbox("Bệnh tim mạch")

    if ha_sys is not None and ha_sys >= 140 and not hypertension:
        st.caption(
            "💡 Huyết áp đo được cao — nếu đã được bác sĩ chẩn đoán cao huyết áp, "
            "hãy tích vào ô trên."
        )


# ╔══════════════════════════════════════════════════════════════════════╗
# ║  7. PHẦN C — TRIỆU CHỨNG FAST                                        ║
# ╚══════════════════════════════════════════════════════════════════════╝

with st.container(border=True):
    card("C  —  Triệu chứng FAST")

    st.markdown(
        "Đây là **4 dấu hiệu cảnh báo đột quỵ** quan trọng nhất.  \n"
        "Kéo thanh trượt sang phải nếu người bệnh *đang có* triệu chứng đó."
    )
    st.write("")

    c_f, c_a = st.columns(2)
    with c_f:
        face_lbl = st.select_slider(
            "F — Méo miệng",
            options=FAST_OPTS, value="Không",
        )
    with c_a:
        arm_lbl = st.select_slider(
            "A — Yếu / liệt tay hoặc chân",
            options=FAST_OPTS, value="Không",
        )

    c_s, c_h = st.columns(2)
    with c_s:
        speech_lbl = st.select_slider(
            "S — Nói khó / nói đớ",
            options=FAST_OPTS, value="Không",
        )
    with c_h:
        head_lbl = st.select_slider(
            "T — Đau đầu dữ dội, đột ngột",
            options=FAST_OPTS, value="Không",
        )

    # Tóm tắt trực quan
    st.write("")
    pill_labels = [
        ("Méo miệng", face_lbl),
        ("Yếu tay/chân", arm_lbl),
        ("Nói khó", speech_lbl),
        ("Đau đầu", head_lbl),
    ]
    cf1, cf2, cf3, cf4 = st.columns(4)
    for col, (name, lbl) in zip([cf1, cf2, cf3, cf4], pill_labels):
        col.markdown(
            f"{pill_html(lbl, FAST_PILL[lbl])}<br>"
            f"<small style='color:#555;font-size:.9rem;'>{name}</small>",
            unsafe_allow_html=True,
        )


# ╔══════════════════════════════════════════════════════════════════════╗
# ║  8. NÚT KIỂM TRA                                                     ║
# ╚══════════════════════════════════════════════════════════════════════╝

st.write("")
run = st.button("🔍  KIỂM TRA NGUY CƠ ĐỘT QUỴ", type="primary", use_container_width=True)
if not run:
    st.stop()


# ╔══════════════════════════════════════════════════════════════════════╗
# ║  9. TÍNH ĐIỂM                                                        ║
# ╚══════════════════════════════════════════════════════════════════════╝

face_v     = FAST_INT[face_lbl]
arm_v      = FAST_INT[arm_lbl]
speech_v   = FAST_INT[speech_lbl]
headache_v = FAST_INT[head_lbl]
fast_max   = max(face_v, arm_v, speech_v, headache_v)

feat_names = meta["feature_names"]
scaler_obj = meta["scaler"]

df_row = build_row(
    age=tuoi, gender=gender, work_type=work_type,
    smoking_status=smoking_status,
    hypertension=hypertension, heart_disease=heart_disease,
    avg_glucose_level=avg_glucose, bmi=bmi,
    feature_names=feat_names,
)

proba    = get_ml_proba(df_row, scaler_obj, model)
ml_score = int(proba * 100)
fast_s   = calc_fast_pts(face_v, arm_v, speech_v, headache_v)
combined = int(ml_score * 0.6 + fast_s * 0.4)

# Bonus huyết áp đo trực tiếp (tối đa +20)
bp_bonus = 0
if ha_sys is not None:
    overrun  = max(0, int(ha_sys) - 115)
    bp_bonus = min(20, int((overrun / 10) ** 2.2))

final_score = min(99, combined + bp_bonus)

# Safety override
override_msg = None
if fast_max == 3:
    final_score  = 99
    override_msg = (
        "CẢNH BÁO: Triệu chứng FAST ở mức NẶNG — tình trạng CỰC KỲ KHẨN CẤP.\n"
        "GỌI CẤP CỨU 115 NGAY LẬP TỨC!"
    )
elif fast_max == 2 and final_score < 80:
    final_score  = 80
    override_msg = (
        "Lưu ý: Triệu chứng FAST ở mức RÕ — "
        "điểm nguy cơ được điều chỉnh lên tối thiểu 80/100 để đảm bảo an toàn."
    )

color_hex, level_label, st_type = get_score_meta(final_score)


# ╔══════════════════════════════════════════════════════════════════════╗
# ║  10. KẾT QUẢ                                                         ║
# ╚══════════════════════════════════════════════════════════════════════╝

st.divider()
st.header("Kết quả đánh giá")

# Mức độ
if st_type == "error":
    st.error(f"**{level_label}**", icon="🔴")
elif st_type == "warning":
    st.warning(f"**{level_label}**", icon="🟠")
else:
    st.success(f"**{level_label}**", icon="🟢")

# Thanh điểm
render_score_bar(final_score, color_hex)


# Override
if override_msg:
    st.markdown(
        f'<div class="override-box">'
        f'{override_msg.replace(chr(10), "<br>")}'
        f'</div>',
        unsafe_allow_html=True,
    )

st.divider()

# Lời khuyên
if final_score >= 70:
    st.error("### Hành động khẩn cấp")
    st.markdown("""
- **Gọi cấp cứu 115 ngay — không chờ đợi thêm.**
- Đặt người bệnh nằm nghiêng, đầu nâng nhẹ khoảng 30°.
- **Không** cho ăn uống bất kỳ thứ gì, kể cả thuốc hay nước lọc.
- **Không** tự ý truyền dịch hoặc tiêm thuốc.
- Ghi lại **giờ xuất hiện triệu chứng đầu tiên** — rất quan trọng với bác sĩ.
""")
elif final_score >= 50:
    st.error("### Đến cơ sở y tế ngay hôm nay")
    st.markdown("""
- Đến bệnh viện hoặc phòng khám **trong vòng 1–2 giờ tới.**
- Theo dõi triệu chứng liên tục, ghi lại diễn biến.
- Nếu đang uống thuốc huyết áp, **tiếp tục uống đúng liều**.
- Nếu triệu chứng FAST nặng hơn → **gọi 115 ngay.**
""")
elif final_score >= 30:
    st.warning("### Cần theo dõi sát")
    st.markdown("""
- Liên hệ bác sĩ hoặc trạm y tế xã **trong ngày hôm nay.**
- Đo huyết áp mỗi 2–3 giờ, ghi lại kết quả.
- Uống đủ nước (1.5–2 lít/ngày), nghỉ ngơi, tránh gắng sức.
- Nếu xuất hiện méo miệng, yếu tay/chân, nói khó → **đi cấp cứu ngay.**
""")
else:
    st.success("### Nguy cơ thấp — tiếp tục theo dõi")
    st.markdown("""
- Nghỉ ngơi, ăn uống nhẹ nhàng, uống đủ nước.
- Theo dõi trong 24–48 giờ tới.
- Kiểm tra huyết áp định kỳ mỗi ngày.
- Nếu xuất hiện triệu chứng mới, hãy liên hệ cơ sở y tế gần nhất.
""")

st.divider()


# ╔══════════════════════════════════════════════════════════════════════╗
# ║  11. XAI                                                             ║
# ╚══════════════════════════════════════════════════════════════════════╝

with st.expander("Phân tích chi tiết đóng góp từng yếu tố (Explainable AI)", expanded=True):
    st.markdown(
        "Biểu đồ dưới đây cho thấy **yếu tố nào đóng góp nhiều nhất** "
        "vào kết quả dự đoán.  \n"
        "Tính theo: `|hệ số hồi quy × giá trị đã chuẩn hóa|`"
    )
    st.caption(
        f"Tổng điểm: **{final_score}/100**  ·  "
        f"ML: {ml_score}/100  ·  "
        f"FAST: {fast_s}/100  ·  "
        f"Huyết áp bonus: +{bp_bonus}"
    )
    xai_ml   = calc_xai_groups(df_row, meta)
    xai_fast = {
        "Méo miệng (F)"    : round(face_v     ** 2 * 0.85, 2),
        "Yếu tay/chân (A)" : round(arm_v      ** 2 * 0.85, 2),
        "Nói khó (S)"      : round(speech_v   ** 2 * 0.85, 2),
        "Đau đầu (T)"      : round(headache_v ** 2 * 0.85, 2),
    }

    all_vals = {**xai_ml, **xai_fast}
    max_v    = max(all_vals.values()) if all_vals else 1

    st.markdown("**Yếu tố nền — mô hình ML (60%)**")
    for name, val in sorted(xai_ml.items(), key=lambda x: -x[1]):
        render_xai_row(name, val, max_v, XAI_COLORS.get(name, "#888780"))

    st.markdown("---")
    st.markdown("**Triệu chứng FAST (40%)**")
    for name, val in xai_fast.items():
        render_xai_row(name, val, max_v, "#C0392B")

st.divider()


# ╔══════════════════════════════════════════════════════════════════════╗
# ║  12. TÌM BỆNH VIỆN                                                   ║
# ╚══════════════════════════════════════════════════════════════════════╝

with st.container(border=True):
    card("Tìm cơ sở y tế gần nhất")
    st.markdown(
        "Nhập tên quận / huyện / thành phố để mở Google Maps và tìm "
        "bệnh viện hoặc cơ sở cấp cứu gần bạn."
    )
    city = st.text_input(
        "Khu vực của bạn",
        placeholder="Ví dụ: Quận 1 TP HCM  ·  Hoàn Kiếm Hà Nội  ·  Biên Hòa Đồng Nai",
        label_visibility="collapsed",
    )
    query    = (
        f"bệnh viện {city.strip()}"
        if city.strip()
        else "bệnh viện gần nhất"
    )
    maps_url = "https://www.google.com/maps/search/" + query.replace(" ", "+")
    st.link_button(
        "Mở bản đồ — tìm bệnh viện gần nhất",
        url=maps_url,
        use_container_width=True,
    )
    st.caption("Trên điện thoại, Google Maps sẽ dùng GPS để tìm bệnh viện gần nhất.")

st.divider()
st.caption(
    "⚕️ Công cụ này chỉ mang tính **sàng lọc hỗ trợ**, "
    "không thay thế chẩn đoán của bác sĩ. "
    "Khi có nghi ngờ đột quỵ, hãy đến cơ sở y tế ngay lập tức."
)