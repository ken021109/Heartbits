import streamlit as st
import math
from datetime import datetime

# 1. config and constant
HE_SO_TUOI = 20.0
MU_TUOI = 1.5
NGUONG_HA_AN_TOAN = 115
DON_VI_CHIA_HA = 10.0
MU_HUYET_AP = 2.2
HE_SO_NHAN_TRIEU_CHUNG = 5.0
DIEM_BENH_NEN = 10.0
DIEM_DAU_DAU_KHUNG_KHI = 25.0


# 2. setting and theme
def cai_dat_giao_dien():
    st.set_page_config(page_title="Stroke Alert VN", page_icon="🧠", layout="centered")

    #setup theme
    with st.sidebar:
        st.header("⚙️ Cài đặt hiển thị")
        theme_mode = st.radio("Chế độ màn hình:", ["Mặc định", "Tương phản cao (Người già)"])

        st.info("""
        💡 **Mẹo:** 
        Để chuyển nền Đen/Trắng của hệ thống:
        Vào dấu 3 chấm (Góc phải trên) > Settings > Theme.
        """)

    #hinh chu to ra
    custom_css = """
    <style>
        /* Tăng cỡ chữ cho các nhãn (Label) */
        .stRadio label, .stCheckbox label, .stNumberInput label, .stSelectbox label, p {
            font-size: 19px !important;
        }
        /* Tăng cỡ chữ trong ô input */
        .stNumberInput input {
            font-size: 20px !important;
            font-weight: bold;
        }
        /* Tăng cỡ chữ thanh trượt */
        .stSlider div[data-baseweb="slider"] div {
            font-size: 18px !important;
        }
        /* Chỉnh nút bấm to ra */
        .stButton button {
            font-size: 22px !important;
            padding: 15px 30px !important; 
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    if theme_mode == "Tương phản cao (Người già)":
        high_contrast_css = """
        <style>
            .stApp {
                background-color: #FFFFFF;
                color: #000000;
            }
            p, label, h1, h2, h3 {
                color: #000000 !important;
                font-weight: 600 !important;
            }
        </style>
        """
        st.markdown(high_contrast_css, unsafe_allow_html=True)

    st.title("🧠 Stroke Alert VN")
    st.markdown("### Ứng dụng hỗ trợ người cao tuổi")
    st.divider()


def huong_dan_do_huyet_ap():
    with st.expander("❓ HƯỚNG DẪN ĐO HUYẾT ÁP (Bấm xem)", expanded=False):
        st.markdown("""
        1. Nghỉ ngơi 5 phút.
        2. Đặt tay lên bàn ngang tim.
        3. **Số trên (SYS):** Tâm thu.
        4. **Số dưới (DIA):** Tâm trương.
        """)


def map_muc_do(text):
    mapping = {"Không": 0, "Nhẹ": 1, "Rõ": 2, "Nặng": 3}
    return mapping.get(text, 0)

# 3. input
def lay_thong_tin():
    data = {}

    st.header("1. Thông tin cá nhân")
    c1, c2 = st.columns([2, 1])
    with c1:
        nam_hien_tai = datetime.now().year
        nam_sinh = st.number_input("Năm sinh (Ví dụ: 1960):", 1900, nam_hien_tai, 1960)
        data['tuoi'] = nam_hien_tai - nam_sinh
    with c2:
        st.write("")  # Cách dòng ra
        st.write("")
        st.write(f"**{data['tuoi']} tuổi**")

    st.write("---")
    st.header("2. Huyết áp & Bệnh nền")

    data['co_so_do_ha'] = st.checkbox("Tôi CÓ máy đo huyết áp lúc này", value=True)

    if data['co_so_do_ha']:
        huong_dan_do_huyet_ap()
        c_ha1, c_ha2 = st.columns(2)
        with c_ha1:
            data['ha_tam_thu'] = st.number_input("Số trên (Tâm thu):", 80, 260, 120)
        with c_ha2:
            data['ha_tam_truong'] = st.number_input("Số dưới (Tâm trương):", 40, 160, 80)
    else:
        st.info("Sẽ đánh giá dựa trên triệu chứng.")
        data['ha_tam_thu'] = 0

    st.caption("Chọn các bệnh đã có:")
    c_b1, c_b2 = st.columns(2)
    benh_cnt = 0
    with c_b1:
        if st.checkbox("Cao huyết áp"): benh_cnt += 1
        if st.checkbox("Tiểu đường"): benh_cnt += 1
    with c_b2:
        if st.checkbox("Bệnh tim mạch"): benh_cnt += 1
        if st.checkbox("Mỡ máu/Thuốc lá"): benh_cnt += 1
    data['so_luong_benh_nen'] = benh_cnt

    st.write("---")
    st.header("3. Triệu chứng (Kéo thanh trượt)")

    thang_do = ["Không", "Nhẹ", "Rõ", "Nặng"]

    st.subheader("Méo miệng (Face):")
    data['face_lv'] = map_muc_do(
        st.select_slider("Mức độ méo miệng:", options=thang_do, value="Không", label_visibility="collapsed"))

    st.subheader("Yếu tay/chân (Arm):")
    data['arm_lv'] = map_muc_do(
        st.select_slider("Mức độ yếu liệt:", options=thang_do, value="Không", label_visibility="collapsed"))

    st.subheader("Nói khó/Đớ (Speech):")
    data['speech_lv'] = map_muc_do(
        st.select_slider("Mức độ nói khó:", options=thang_do, value="Không", label_visibility="collapsed"))

    st.write("---")
    data['dau_dau_du_doi'] = st.checkbox("Đau đầu dữ dội, đột ngột?")

    return data

# 4. calc
def tinh_toan(data):
    diem_tuoi = (data['tuoi'] / 100) ** MU_TUOI * HE_SO_TUOI
    diem_benh = data['so_luong_benh_nen'] * DIEM_BENH_NEN

    diem_ha = 0
    if data['co_so_do_ha']:
        muc_chenh = max(0, data['ha_tam_thu'] - NGUONG_HA_AN_TOAN)
        diem_ha = (muc_chenh / DON_VI_CHIA_HA) ** MU_HUYET_AP

    tong_fast = (data['face_lv'] ** 2) + (data['arm_lv'] ** 2) + (data['speech_lv'] ** 2)
    diem_trieu_chung = tong_fast * HE_SO_NHAN_TRIEU_CHUNG
    diem_dau_dau = DIEM_DAU_DAU_KHUNG_KHI if data['dau_dau_du_doi'] else 0

    tong_diem = diem_tuoi + diem_benh + diem_ha + diem_trieu_chung + diem_dau_dau
    return min(100, int(tong_diem))



# 5. hien thi ket qua
def hien_thi_ket_qua(score):
    st.divider()
    st.header("KẾT QUẢ ĐÁNH GIÁ")

    # Thanh hiển thị
    st.progress(score, text=f"Thang điểm rủi ro: {score}/100")

    if score >= 60:
        st.error("🔴 NGUY CƠ CAO (RED)")
        with st.container(border=True):
            st.markdown("""
            ### 📞 HÀNH ĐỘNG KHẨN CẤP:
            *   🚑 **Đưa người bệnh đến cơ sở y tế NGAY.**
            *   🌡️ Hạ sốt bằng paracetamol (KHÔNG dùng aspirin).
            *   🛌 Cho người bệnh nằm nghiêng, tránh co giật.
            *   🚫 Không tự ý truyền dịch.
            *   📞 Liên hệ trạm y tế xã / cấp cứu.
            """)

    elif score >= 20:
        st.warning("🟠 NGUY CƠ TRUNG BÌNH (ORANGE)")
        with st.container(border=True):
            st.markdown("""
            ### ⚠️ CẦN THEO DÕI SÁT:
            *   🌡️ Theo dõi nhiệt độ mỗi 2–3 giờ.
            *   💧 Uống nhiều nước / oresol.
            *   🛌 Nghỉ ngơi, tránh ánh sáng mạnh.
            *   ⚠️ **Nếu xuất hiện cứng cổ, lú lẫn → ĐI KHÁM NGAY.**
            """)

    else:
        st.success("🟢 NGUY CƠ THẤP (GREEN)")
        with st.container(border=True):
            st.markdown("""
            ### ✅ LỜI KHUYÊN:
            *   😌 Nghỉ ngơi, ăn uống nhẹ.
            *   👀 Theo dõi triệu chứng trong 48 giờ.
            *   🦟 Tránh muỗi đốt (màn, thuốc xịt).
            *   📍 Báo y tế địa phương nếu sốt tái phát.
            """)



# main
def main():
    cai_dat_giao_dien()
    data = lay_thong_tin()

    # CSS Hack cho nút bấm to
    st.write("")
    if st.button("🔍 BẤM VÀO ĐÂY ĐỂ KIỂM TRA", type="primary", use_container_width=True):
        kq = tinh_toan(data)
        hien_thi_ket_qua(kq)


if __name__ == "__main__":
    main()