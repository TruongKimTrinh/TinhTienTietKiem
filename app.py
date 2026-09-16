import streamlit as st

# ==============================
# CẤU HÌNH TRANG
# ==============================
st.set_page_config(
    page_title="Tính tiền gửi tiết kiệm",
    page_icon="🏦",
    layout="wide"
)

# ==============================
# CSS
# ==============================
st.markdown("""
<style>
    .stApp {
        background:
            radial-gradient(circle at 10% 10%, #e7f2ff 0, transparent 25%),
            radial-gradient(circle at 90% 10%, #ddfff6 0, transparent 25%),
            #f7f9fc;
    }

    .block-container {
        max-width: 1150px;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3 {
        color: #0A1B33;
    }

    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #0A1B33;
        margin-bottom: 4px;
        letter-spacing: -1.5px;
    }

    .subtitle {
        color: #6B778C;
        font-size: 16px;
        margin-bottom: 28px;
    }

    /* CARD NHẬP LIỆU */
    div[data-testid="stForm"] {
        background: rgba(255,255,255,0.82);
        border: 1px solid #DCE4EE;
        border-radius: 22px;
        padding: 25px 28px 28px 28px;
        box-shadow: 0 14px 40px rgba(20, 45, 75, 0.06);
    }

    div[data-testid="stNumberInput"] input {
        font-size: 17px;
        font-weight: 650;
        border-radius: 12px;
    }

    /* BUTTON */
    div[data-testid="stFormSubmitButton"] button {
        width: 100%;
        height: 52px;
        border-radius: 13px;
        border: none;
        font-size: 17px;
        font-weight: 700;
        background: linear-gradient(
            90deg,
            #00B389,
            #00A77F
        );
        color: white;
        transition: 0.2s;
    }

    div[data-testid="stFormSubmitButton"] button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 22px rgba(0,179,137,0.22);
        color: white;
    }

    /* KẾT QUẢ */
    .result-title {
        font-size: 30px;
        font-weight: 800;
        color: #0A1B33;
        margin-top: 35px;
        margin-bottom: 20px;
    }

    .result-card {
        background: white;
        border: 1px solid #E1E7EF;
        border-radius: 20px;
        padding: 25px 27px;
        min-height: 270px;
        box-shadow: 0 10px 30px rgba(16, 40, 70, 0.055);
    }

    .result-card.compound {
        border-top: 4px solid #00B389;
    }

    .result-card.simple {
        border-top: 4px solid #16345C;
    }

    .result-card-title {
        font-size: 24px;
        font-weight: 800;
        color: #0A1B33;
        margin-bottom: 25px;
    }

    .small-label {
        color: #6A788D;
        font-size: 14px;
        margin-bottom: 5px;
    }

    .interest-value {
        color: #0A1B33;
        font-size: 31px;
        font-weight: 800;
        margin-bottom: 24px;
        font-variant-numeric: tabular-nums;
    }

    .total-value {
        color: #00A77F;
        font-size: 30px;
        font-weight: 800;
        font-variant-numeric: tabular-nums;
    }

    .extra {
        display: inline-block;
        background: #E6FAF4;
        color: #008765;
        border-radius: 999px;
        padding: 7px 12px;
        font-weight: 700;
        font-size: 13px;
        margin-top: 10px;
    }

    /* TÓM TẮT */
    .summary-title {
        font-size: 27px;
        font-weight: 800;
        color: #0A1B33;
        margin-top: 32px;
        margin-bottom: 15px;
    }

    .highlight {
        background: linear-gradient(135deg, #E5FAF4, #F1FFFB);
        border: 1px solid #B9EFE1;
        padding: 16px 20px;
        border-radius: 15px;
        color: #08765E;
        font-weight: 650;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    /* EXPANDER */
    div[data-testid="stExpander"] {
        background: white;
        border: 1px solid #E1E7EF;
        border-radius: 15px;
        overflow: hidden;
    }

    /* MOBILE */
    @media (max-width: 768px) {
        .block-container {
            padding: 1.2rem;
        }

        .main-title {
            font-size: 31px;
        }

        .interest-value,
        .total-value {
            font-size: 25px;
        }

        .result-card {
            min-height: auto;
        }
    }
</style>
""", unsafe_allow_html=True)


# ==============================
# HÀM FORMAT TIỀN
# ==============================
def money(value):
    return f"{value:,.0f} VNĐ"


# ==============================
# TIÊU ĐỀ
# ==============================
st.markdown(
    '<div class="main-title">🏦 Tính tiền gửi tiết kiệm</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Tính toán và so sánh lợi nhuận giữa lãi đơn và lãi kép.'
    '</div>',
    unsafe_allow_html=True
)


# ==============================
# FORM NHẬP
# ==============================
with st.form("saving_form"):

    st.markdown("### Thông tin khoản tiết kiệm")

    st.caption(
        "Nhập số tiền, thời gian gửi và lãi suất để xem kết quả."
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:
        so_tien = st.number_input(
            "Số tiền gửi (VNĐ)",
            min_value=0,
            value=100_000_000,
            step=1_000_000,
            format="%d"
        )

        so_thang = st.number_input(
            "Thời gian gửi (tháng)",
            min_value=1,
            max_value=360,
            value=12,
            step=1
        )

    with col2:
        lai_suat = st.number_input(
            "Lãi suất (%/năm)",
            min_value=0.0,
            max_value=100.0,
            value=5.90,
            step=0.10,
            format="%.2f"
        )

        st.write("")
        st.write("")

        st.info(
            f"Khoản gửi hiện tại: **{so_tien:,.0f} VNĐ**"
        )

    st.write("")

    submit = st.form_submit_button(
        "Tính toán"
    )


# ==============================
# XỬ LÝ
# ==============================
if submit:

    if so_tien <= 0:
        st.error("Số tiền gửi phải lớn hơn 0.")
        st.stop()

    if so_thang <= 0:
        st.error("Thời gian gửi phải lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.stop()

    # ==============================
    # TÍNH TOÁN
    # ==============================
    r_nam = lai_suat / 100
    so_nam = so_thang / 12

    # Lãi đơn
    lai_don = so_tien * r_nam * so_nam
    tong_lai_don = so_tien + lai_don

    # Lãi kép - gộp hàng tháng
    r_thang = r_nam / 12

    tong_lai_kep = (
        so_tien *
        (1 + r_thang) ** so_thang
    )

    lai_kep = tong_lai_kep - so_tien

    # Chênh lệch
    chenh_lech = tong_lai_kep - tong_lai_don


    # ==============================
    # KẾT QUẢ
    # ==============================
    st.markdown(
        '<div class="result-title">Kết quả</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2, gap="large")


    # ------------------------------
    # LÃI ĐƠN
    # ------------------------------
    with col1:

        st.markdown(
            f"""
            <div class="result-card simple">

                <div class="result-card-title">
                    Lãi đơn
                </div>

                <div class="small-label">
                    Tiền lãi nhận được
                </div>

                <div class="interest-value">
                    {money(lai_don)}
                </div>

                <div class="small-label">
                    Tổng số tiền nhận được
                </div>

                <div class="total-value">
                    {money(tong_lai_don)}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # ------------------------------
    # LÃI KÉP
    # ------------------------------
    with col2:

        extra_html = ""

        if chenh_lech > 0:
            extra_html = f"""
            <div class="extra">
                + {money(chenh_lech)} so với lãi đơn
            </div>
            """

        st.markdown(
            f"""
            <div class="result-card compound">

                <div class="result-card-title">
                    Lãi kép
                    <span style="
                        font-size:14px;
                        color:#738196;
                        font-weight:500;
                    ">
                        (gộp tháng)
                    </span>
                </div>

                <div class="small-label">
                    Tiền lãi nhận được
                </div>

                <div class="interest-value">
                    {money(lai_kep)}
                </div>

                <div class="small-label">
                    Tổng số tiền nhận được
                </div>

                <div class="total-value">
                    {money(tong_lai_kep)}
                </div>

                {extra_html}

            </div>
            """,
            unsafe_allow_html=True
        )


    # ==============================
    # TÓM TẮT
    # ==============================
    st.markdown(
        '<div class="summary-title">Tóm tắt kết quả</div>',
        unsafe_allow_html=True
    )

    summary = {
        "Phương thức": [
            "Lãi đơn",
            "Lãi kép"
        ],
        "Tiền gốc (VNĐ)": [
            f"{so_tien:,.0f}",
            f"{so_tien:,.0f}"
        ],
        "Tiền lãi (VNĐ)": [
            f"{lai_don:,.0f}",
            f"{lai_kep:,.0f}"
        ],
        "Tổng tiền (VNĐ)": [
            f"{tong_lai_don:,.0f}",
            f"{tong_lai_kep:,.0f}"
        ]
    }

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )


    # ==============================
    # CHÊNH LỆCH
    # ==============================
    if chenh_lech > 0:

        st.markdown(
            f"""
            <div class="highlight">
                Với khoản gửi {money(so_tien)} trong
                {so_thang} tháng ở mức lãi suất
                {lai_suat:.2f}%/năm, lãi kép cho tổng
                số tiền cao hơn lãi đơn
                <strong>{money(chenh_lech)}</strong>.
            </div>
            """,
            unsafe_allow_html=True
        )


    # ==============================
    # CHI TIẾT CÁCH TÍNH
    # ==============================
    with st.expander("Xem chi tiết cách tính"):

        st.markdown("### Lãi đơn")

        st.latex(
            r"A = P(1 + rt)"
        )

        st.write(
            f"""
            - P = {money(so_tien)}
            - r = {r_nam:.4f}
            - t = {so_thang}/12 = {so_nam:.2f} năm
            """
        )

        st.code(
            f"A = {so_tien:,.0f} × "
            f"(1 + {r_nam:.4f} × {so_nam:.2f})"
        )

        st.write(
            f"**Tổng tiền: {money(tong_lai_don)}**"
        )

        st.divider()

        st.markdown("### Lãi kép")

        st.latex(
            r"A = P(1 + r/12)^n"
        )

        st.write(
            f"""
            - P = {money(so_tien)}
            - r = {r_nam:.4f}
            - n = {so_thang} tháng
            - Lãi suất tháng = {r_thang * 100:.4f}%
            """
        )

        st.code(
            f"A = {so_tien:,.0f} × "
            f"(1 + {r_thang:.6f})^{so_thang}"
        )

        st.write(
            f"**Tổng tiền: {money(tong_lai_kep)}**"
        )


# ==============================
# FOOTER
# ==============================
st.markdown("<br><br>", unsafe_allow_html=True)

st.caption(
    "Số liệu chỉ mang tính chất tham khảo, "
    "không phải cam kết lãi suất thực tế."
)
