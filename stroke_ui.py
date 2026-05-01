import streamlit as st


def render_score_bar(score: int, color: str):
    st.markdown(
        f'<div class="score-wrap">'
        f'<div class="score-fill" style="width:{score}%;background:{color};">'
        f"{score} / 100</div></div>",
        unsafe_allow_html=True,
    )


def render_result_section(
    final_score: int,
    color_hex: str,
    level_label: str,
    status_type: str,
    override_msg: str | None,
):
    st.divider()
    st.header("Kết quả đánh giá")

    if status_type == "error":
        st.error(f"**{level_label}**", icon="🔴")
    elif status_type == "warning":
        st.warning(f"**{level_label}**", icon="🟠")
    else:
        st.success(f"**{level_label}**", icon="🟢")

    render_score_bar(final_score, color_hex)

    if override_msg:
        st.markdown(
            f'<div class="override-box">'
            f'{override_msg.replace(chr(10), "<br>")}'
            f"</div>",
            unsafe_allow_html=True,
        )

    st.divider()
    _render_medical_advice(final_score)
    st.divider()


def _render_medical_advice(final_score: int):
    if final_score >= 70:
        st.error("### Hành động khẩn cấp")
        st.markdown(
            """
- **Gọi cấp cứu 115 ngay — không chờ đợi thêm.**
- Đặt người bệnh nằm nghiêng, đầu nâng nhẹ khoảng 30°.
- **Không** cho ăn uống bất kỳ thứ gì, kể cả thuốc hay nước lọc.
- **Không** tự ý truyền dịch hoặc tiêm thuốc.
- Ghi lại **giờ xuất hiện triệu chứng đầu tiên** — rất quan trọng với bác sĩ.
"""
        )
    elif final_score >= 50:
        st.error("### Đến cơ sở y tế ngay hôm nay")
        st.markdown(
            """
- Đến bệnh viện hoặc phòng khám **trong vòng 1–2 giờ tới.**
- Theo dõi triệu chứng liên tục, ghi lại diễn biến.
- Nếu đang uống thuốc huyết áp, **tiếp tục uống đúng liều**.
- Nếu triệu chứng FAST nặng hơn → **gọi 115 ngay.**
"""
        )
    elif final_score >= 30:
        st.warning("### Cần theo dõi sát")
        st.markdown(
            """
- Liên hệ bác sĩ hoặc trạm y tế xã **trong ngày hôm nay.**
- Đo huyết áp mỗi 2–3 giờ, ghi lại kết quả.
- Uống đủ nước (1.5–2 lít/ngày), nghỉ ngơi, tránh gắng sức.
- Nếu xuất hiện méo miệng, yếu tay/chân, nói khó → **đi cấp cứu ngay.**
"""
        )
    else:
        st.success("### Nguy cơ thấp — tiếp tục theo dõi")
        st.markdown(
            """
- Nghỉ ngơi, ăn uống nhẹ nhàng, uống đủ nước.
- Theo dõi trong 24–48 giờ tới.
- Kiểm tra huyết áp định kỳ mỗi ngày.
- Nếu xuất hiện triệu chứng mới, hãy liên hệ cơ sở y tế gần nhất.
"""
        )
