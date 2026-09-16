import streamlit as st
from datetime import datetime

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Tiết kiệm có kỳ hạn",
    page_icon="🏦",
    layout="wide"
)

# =========================================================
# SESSION STATE
# =========================================================
if "history" not in st.session_state:
    st.session_state.history = []

if "result" not in st.session_state:
    st.session_state.result = None


# =========================================================
# FUNCTIONS
# =========================================================
def format_money(value):
    return f"{value:,.0f}".replace(",", ".") + " đ"


def calculate(principal, months, rate):
    annual_rate = rate / 100
    years = months / 12

    # Lãi đơn
    simple_interest = principal * annual_rate * years
    simple_total = principal + simple_interest

    # Lãi kép theo tháng
    monthly_rate = annual_rate / 12
    compound_total = principal * (1 + monthly_rate) ** months
    compound_interest = compound_total - principal

    difference = compound_total - simple_total

    return {
        "principal": principal,
        "months": months,
        "rate": rate,
        "simple_interest": simple_interest,
        "simple_total": simple_total,
        "compound_interest": compound_interest,
        "compound_total": compound_total,
        "difference": difference,
        "annual_rate": annual_rate,
        "monthly_rate": monthly_rate,
        "years": years,
        "time": datetime.now().strftime("%H:%M - %d/%m/%Y")
    }


# =========================================================
# CSS
# =========================================================
st.markdown("""
<style>

/* =========================
   GLOBAL
========================= */

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(37, 99, 235, .16), transparent 28%),
        radial-gradient(circle at 90% 15%, rgba(0, 179, 137, .18), transparent 27%),
        radial-gradient(circle at 50% 95%, rgba(99, 102, 241, .10), transparent 30%),
        #F5F8FC;
}

.block-container {
    max-width: 1100px;
    padding-top: 2.2rem;
    padding-bottom: 5rem;
}

/* Font */
html, body, [class*="css"] {
    font-family: "Segoe UI", sans-serif;
}

/* =========================
   HEADER
========================= */

.main-header {
    padding: 8px 4px 26px 4px;
}

.main-title {
    font-size: 43px;
    font-weight: 900;
    letter-spacing: -1.8px;
    color: #081C35;
    line-height: 1.05;
}

.gradient-text {
    background: linear-gradient(
        90deg,
        #0066FF,
        #00B389
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    margin-top: 12px;
    color: #718096;
    font-size: 16px;
}

/* =========================
   FORM
========================= */

div[data-testid="stForm"] {
    background: rgba(255,255,255,.82);
    backdrop-filter: blur(18px);

    border: 1px solid rgba(255,255,255,.9);

    border-radius: 25px;

    padding: 28px;

    box-shadow:
        0 20px 60px rgba(13, 38, 76, .10),
        inset 0 1px 0 rgba(255,255,255,.8);
}

div[data-testid="stNumberInput"] input {
    background: #F6F9FD;
    border-radius: 12px;
    font-weight: 700;
    font-size: 16px;
}

/* =========================
   BUTTON
========================= */

div[data-testid="stFormSubmitButton"] button {

    height: 55px;

    border: none;
    border-radius: 15px;

    font-size: 16px;
    font-weight: 800;

    color: white;

    background:
        linear-gradient(
            90deg,
            #006BFF,
            #00B389
        );

    box-shadow:
        0 12px 30px rgba(0,179,137,.25);

    transition: all .2s ease;
}

div[data-testid="stFormSubmitButton"] button:hover {

    color: white;

    transform: translateY(-2px);

    box-shadow:
        0 16px 35px rgba(0,179,137,.35);
}

/* =========================
   RESULT AREA
========================= */

.result-heading {
    margin-top: 38px;
    margin-bottom: 18px;

    font-size: 32px;
    font-weight: 900;

    color: #081C35;
}

.result-box {

    background:
        linear-gradient(
            145deg,
            #0A1B33,
            #123D66 58%,
            #008B76
        );

    border-radius: 25px;

    padding: 28px;

    color: white;

    box-shadow:
        0 20px 50px rgba(10,27,51,.20);

    position: relative;
    overflow: hidden;
}

.result-box::before {

    content: "";

    position: absolute;

    width: 220px;
    height: 220px;

    right: -80px;
    top: -90px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(73,255,214,.30),
            transparent 65%
        );
}

.result-type {
    font-size: 15px;
    font-weight: 700;

    color: rgba(255,255,255,.72);
}

.result-interest {

    font-size: 27px;
    font-weight: 800;

    margin-top: 7px;

    color: white;
}

.result-label {

    font-size: 13px;

    color: rgba(255,255,255,.65);

    margin-top: 22px;
}

.result-total {

    font-size: 34px;
    font-weight: 900;

    margin-top: 3px;

    color: #5FFFD7;

    letter-spacing: -1px;
}

.badge {

    display: inline-block;

    margin-top: 17px;

    padding: 7px 13px;

    border-radius: 999px;

    background: rgba(95,255,215,.14);

    border: 1px solid rgba(95,255,215,.25);

    color: #70FFDB;

    font-size: 13px;

    font-weight: 800;
}

/* =========================
   SUMMARY
========================= */

.summary-box {

    margin-top: 25px;

    padding: 21px 24px;

    border-radius: 18px;

    background:
        linear-gradient(
            135deg,
            rgba(225,255,247,.95),
            rgba(239,248,255,.95)
        );

    border: 1px solid #C8F1E6;

    box-shadow:
        0 10px 30px rgba(0,179,137,.07);
}

.summary-title {

    font-weight: 850;

    font-size: 16px;

    color: #087A62;
}

.summary-value {

    margin-top: 7px;

    font-size: 23px;

    font-weight: 900;

    color: #063D36;
}

/* =========================
   HISTORY
========================= */

.history-title {

    margin-top: 45px;

    font-size: 31px;

    font-weight: 900;

    color: #081C35;
}

.history-card {

    padding: 20px 23px;

    margin-top: 13px;

    background: rgba(255,255,255,.92);

    border: 1px solid #E1EAF3;

    border-radius: 18px;

    box-shadow:
        0 9px 25px rgba(19,45,80,.06);
}

.history-date {

    font-size: 12px;

    font-weight: 700;

    color: #8996A8;
}

.history-money {

    margin-top: 5px;

    font-size: 22px;

    font-weight: 900;

    color: #0A1B33;
}

.history-info {

    margin-top: 7px;

    color: #627187;

    font-size: 14px;
}

/* =========================
   EXPANDER
========================= */

div[data-testid="stExpander"] {

    background: rgba(255,255,255,.9);

    border-radius: 16px;

    border: 1px solid #DFE7F0;

    overflow: hidden;
}

/* =========================
   DATAFRAME
========================= */

div[data-testid="stDataFrame"] {

    border-radius: 15px;

    overflow: hidden;
}

/* =========================
   MOBILE
========================= */

@media (max-width: 768px) {

    .block-container {
        padding: 1.2rem;
    }

    .main-title {
        font-size: 33px;
    }

    .result-total {
        font-size: 27px;
    }

    .result-interest {
        font-size: 23px;
    }

    div[data-testid="stForm"] {
        padding: 19px;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="main-header">
    <div class="main-title">
        Tiết kiệm <span class="gradient-text">thông minh</span>
    </div>
    <div class="subtitle">
        Tính toán và so sánh lợi nhuận tiền gửi của bạn.
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# INPUT FORM
# =========================================================
with st.form("saving_form"):

    st.markdown("## Thông tin tiền gửi")
    st.caption("Nhập thông tin khoản tiết kiệm bạn muốn tính.")

    col1, col2 = st.columns(2, gap="large")

    with col1:

        so_tien = st.number_input(
            "Số tiền gửi (VNĐ)",
            min_value=0,
            value=100_000_000,
            step=1_000_000,
            format="%d"
        )

        st.caption(
            f"Số tiền hiện tại: {format_money(so_tien)}"
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

    so_thang = st.slider(
        "Thời gian gửi",
        min_value=1,
        max_value=36,
        value=12,
        step=1
    )

    st.caption(
        f"Kỳ hạn đang chọn: {so_thang} tháng"
    )

    st.write("")

    submit = st.form_submit_button(
        "Tính tiền tiết kiệm",
        use_container_width=True
    )


# =========================================================
# CALCULATE
# =========================================================
if submit:

    if so_tien <= 0:

        st.error(
            "Vui lòng nhập số tiền gửi lớn hơn 0."
        )

    elif lai_suat < 0:

        st.error(
            "Lãi suất không được nhỏ hơn 0."
        )

    else:

        result = calculate(
            so_tien,
            so_thang,
            lai_suat
        )

        st.session_state.result = result

        # Lưu lịch sử
        st.session_state.history.insert(
            0,
            result.copy()
        )

        # Giới hạn 10 lần gần nhất
        st.session_state.history = (
            st.session_state.history[:10]
        )


# =========================================================
# RESULT
# =========================================================
if st.session_state.result:

    r = st.session_state.result

    st.markdown(
        '<div class="result-heading">Kết quả tính toán</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2, gap="large")


    # =====================================================
    # SIMPLE
    # =====================================================
    with col1:

        simple_html = (
            '<div class="result-box">'
            '<div class="result-type">LÃI ĐƠN</div>'
            '<div class="result-label">Tiền lãi nhận được</div>'
            f'<div class="result-interest">{format_money(r["simple_interest"])}</div>'
            '<div class="result-label">Tổng số tiền nhận được</div>'
            f'<div class="result-total">{format_money(r["simple_total"])}</div>'
            '</div>'
        )

        st.markdown(
            simple_html,
            unsafe_allow_html=True
        )


    # =====================================================
    # COMPOUND
    # =====================================================
    with col2:

        compound_html = (
            '<div class="result-box">'
            '<div class="result-type">LÃI KÉP • GỘP THÁNG</div>'
            '<div class="result-label">Tiền lãi nhận được</div>'
            f'<div class="result-interest">{format_money(r["compound_interest"])}</div>'
            '<div class="result-label">Tổng số tiền nhận được</div>'
            f'<div class="result-total">{format_money(r["compound_total"])}</div>'
            f'<div class="badge">+ {format_money(r["difference"])} so với lãi đơn</div>'
            '</div>'
        )

        st.markdown(
            compound_html,
            unsafe_allow_html=True
        )


    # =====================================================
    # HIGHLIGHT
    # =====================================================
    st.markdown(
        (
            '<div class="summary-box">'
            '<div class="summary-title">'
            'Chênh lệch lợi nhuận'
            '</div>'
            f'<div class="summary-value">{format_money(r["difference"])}</div>'
            '<div style="color:#648176;margin-top:5px;">'
            'Đây là phần tiền tăng thêm khi áp dụng lãi kép theo tháng.'
            '</div>'
            '</div>'
        ),
        unsafe_allow_html=True
    )


    # =====================================================
    # SUMMARY TABLE
    # =====================================================
    st.markdown("### Tổng kết")

    summary = {
        "Phương thức": [
            "Lãi đơn",
            "Lãi kép"
        ],

        "Tiền gốc": [
            format_money(r["principal"]),
            format_money(r["principal"])
        ],

        "Tiền lãi": [
            format_money(r["simple_interest"]),
            format_money(r["compound_interest"])
        ],

        "Tổng nhận": [
            format_money(r["simple_total"]),
            format_money(r["compound_total"])
        ]
    }

    st.dataframe(
        summary,
        hide_index=True,
        use_container_width=True
    )


    # =====================================================
    # FORMULA
    # =====================================================
    with st.expander(
        "Xem chi tiết cách tính"
    ):

        st.markdown("### Lãi đơn")

        st.latex(
            r"A = P(1 + rt)"
        )

        st.write(
            f"""
**P:** {format_money(r["principal"])}

**r:** {r["annual_rate"]:.4f}

**t:** {r["months"]}/12 = {r["years"]:.2f} năm
"""
        )

        st.code(
            f'A = {r["principal"]:,.0f} × '
            f'(1 + {r["annual_rate"]:.4f} × '
            f'{r["years"]:.2f})'
        )

        st.success(
            f'Tổng nhận: {format_money(r["simple_total"])}'
        )

        st.divider()

        st.markdown("### Lãi kép")

        st.latex(
            r"A = P(1+r/12)^n"
        )

        st.write(
            f"""
**P:** {format_money(r["principal"])}

**r:** {r["annual_rate"]:.4f}

**n:** {r["months"]} tháng

**Lãi suất tháng:** {r["monthly_rate"] * 100:.4f}%
"""
        )

        st.code(
            f'A = {r["principal"]:,.0f} × '
            f'(1 + {r["monthly_rate"]:.6f})'
            f'^{r["months"]}'
        )

        st.success(
            f'Tổng nhận: {format_money(r["compound_total"])}'
        )


# =========================================================
# HISTORY
# =========================================================
st.markdown(
    '<div class="history-title">Lịch sử tra cứu</div>',
    unsafe_allow_html=True
)

st.caption(
    "Các phép tính gần đây trong phiên làm việc."
)


if st.session_state.history:

    col_title, col_delete = st.columns(
        [4, 1]
    )

    with col_delete:

        if st.button(
            "Xóa lịch sử",
            use_container_width=True
        ):

            st.session_state.history = []

            st.rerun()


    for index, item in enumerate(
        st.session_state.history
    ):

        history_html = (
            '<div class="history-card">'
            f'<div class="history-date">{item["time"]}</div>'
            f'<div class="history-money">{format_money(item["compound_total"])}</div>'
            '<div class="history-info">'
            f'Gửi <b>{format_money(item["principal"])}</b>'
            f' &nbsp; • &nbsp; {item["months"]} tháng'
            f' &nbsp; • &nbsp; {item["rate"]:.2f}%/năm'
            f' &nbsp; • &nbsp; Lãi kép: <b>{format_money(item["compound_interest"])}</b>'
            '</div>'
            '</div>'
        )

        st.markdown(
            history_html,
            unsafe_allow_html=True
        )

else:

    st.info(
        "Chưa có lịch sử tra cứu. Hãy thực hiện phép tính đầu tiên."
    )


# =========================================================
# FOOTER
# =========================================================
st.markdown("<br>", unsafe_allow_html=True)

st.divider()

st.caption(
    "Số liệu chỉ mang tính chất tham khảo, "
    "không phải cam kết lãi suất thực tế."
)
