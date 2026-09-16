import streamlit as st
from datetime import datetime

# =========================================================
# CẤU HÌNH TRANG
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
# HÀM FORMAT TIỀN
# =========================================================
def format_money(value):
    return f"{value:,.0f}".replace(",", ".") + " đ"


# =========================================================
# HÀM TÍNH TOÁN
# =========================================================
def calculate(principal, months, rate):

    annual_rate = rate / 100
    years = months / 12

    # -------------------------
    # LÃI ĐƠN
    # -------------------------
    simple_interest = (
        principal * annual_rate * years
    )

    simple_total = (
        principal + simple_interest
    )

    # -------------------------
    # LÃI KÉP THEO THÁNG
    # -------------------------
    monthly_rate = annual_rate / 12

    compound_total = (
        principal
        * (1 + monthly_rate) ** months
    )

    compound_interest = (
        compound_total - principal
    )

    difference = (
        compound_total - simple_total
    )

    return {
        "principal": principal,
        "months": months,
        "rate": rate,

        "annual_rate": annual_rate,
        "monthly_rate": monthly_rate,
        "years": years,

        "simple_interest": simple_interest,
        "simple_total": simple_total,

        "compound_interest": compound_interest,
        "compound_total": compound_total,

        "difference": difference,

        "time": datetime.now().strftime(
            "%H:%M - %d/%m/%Y"
        )
    }


# =========================================================
# CSS
# =========================================================
st.markdown(
    """
<style>

/* ========================================================
   NỀN TOÀN TRANG
======================================================== */

.stApp {
    background:
        radial-gradient(
            circle at 8% 8%,
            rgba(0, 107, 255, 0.17),
            transparent 28%
        ),
        radial-gradient(
            circle at 92% 10%,
            rgba(0, 179, 137, 0.18),
            transparent 28%
        ),
        radial-gradient(
            circle at 50% 100%,
            rgba(95, 105, 255, 0.10),
            transparent 32%
        ),
        #F4F8FC !important;

    color: #0A1B33 !important;
}


/* ========================================================
   CONTAINER
======================================================== */

.block-container {

    max-width: 1080px;

    padding-top: 2.4rem;
    padding-bottom: 5rem;
}


/* ========================================================
   TEXT
======================================================== */

h1,
h2,
h3,
h4,
p,
label {

    color: #0A1B33;
}


/* ========================================================
   HEADER
======================================================== */

.main-header {

    padding-top: 5px;
    padding-bottom: 28px;
}


.main-title {

    font-size: 44px;

    font-weight: 900;

    letter-spacing: -2px;

    color: #071C35;

    line-height: 1.08;
}


.gradient-text {

    background:
        linear-gradient(
            90deg,
            #006BFF,
            #00B389
        );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;

    background-clip: text;
}


.subtitle {

    margin-top: 11px;

    color: #6E7C91;

    font-size: 16px;

    font-weight: 500;
}


/* ========================================================
   FORM
======================================================== */

div[data-testid="stForm"] {

    background:
        rgba(255,255,255,0.92) !important;

    border:
        1px solid rgba(210,222,235,0.9);

    border-radius: 26px;

    padding: 30px;

    box-shadow:
        0 22px 60px
        rgba(14,42,76,0.10);

    color: #0A1B33 !important;
}


/* ========================================================
   LABEL INPUT
======================================================== */

div[data-testid="stNumberInput"] label,
div[data-testid="stSlider"] label {

    color: #0A1B33 !important;

    font-weight: 750 !important;

    font-size: 15px !important;
}


/* ========================================================
   NUMBER INPUT
======================================================== */

div[data-testid="stNumberInput"] {

    color: #0A1B33 !important;
}


div[data-testid="stNumberInput"] > div {

    background: #F4F7FB !important;

    border-radius: 13px !important;
}


div[data-testid="stNumberInput"] input {

    background: #F4F7FB !important;

    color: #0A1B33 !important;

    -webkit-text-fill-color:
        #0A1B33 !important;

    caret-color:
        #006BFF !important;

    font-size: 16px !important;

    font-weight: 750 !important;

    min-height: 48px !important;

    border-radius: 12px !important;
}


/* ========================================================
   +/- BUTTON
======================================================== */

div[data-testid="stNumberInput"] button {

    background:
        #F4F7FB !important;

    color:
        #0A1B33 !important;

    border-color:
        #DEE6F0 !important;
}


div[data-testid="stNumberInput"] button svg {

    fill:
        #0A1B33 !important;

    color:
        #0A1B33 !important;
}


/* ========================================================
   CAPTION
======================================================== */

div[data-testid="stCaptionContainer"] {

    color:
        #748297 !important;
}


/* ========================================================
   SLIDER
======================================================== */

div[data-testid="stSlider"] {

    color:
        #0A1B33 !important;
}


/* ========================================================
   NÚT TÍNH
======================================================== */

div[data-testid="stFormSubmitButton"] button {

    width: 100%;

    min-height: 56px;

    border: none;

    border-radius: 16px;

    color: white !important;

    font-size: 16px;

    font-weight: 800;

    background:
        linear-gradient(
            100deg,
            #006BFF 0%,
            #00A7D8 48%,
            #00B389 100%
        ) !important;

    box-shadow:
        0 13px 30px
        rgba(0,160,170,0.26);

    transition:
        all 0.20s ease;
}


div[data-testid="stFormSubmitButton"]
button:hover {

    color:
        white !important;

    transform:
        translateY(-2px);

    box-shadow:
        0 17px 36px
        rgba(0,160,170,0.34);
}


/* ========================================================
   RESULT HEADING
======================================================== */

.result-heading {

    margin-top: 42px;

    margin-bottom: 20px;

    font-size: 32px;

    font-weight: 900;

    color: #071C35;
}


/* ========================================================
   RESULT CARD
======================================================== */

.result-card {

    position: relative;

    overflow: hidden;

    min-height: 300px;

    padding: 29px;

    border-radius: 25px;

    background:
        linear-gradient(
            145deg,
            #081A31 0%,
            #103B63 55%,
            #007E70 100%
        );

    box-shadow:
        0 22px 50px
        rgba(8,26,49,0.20);

    border:
        1px solid
        rgba(255,255,255,0.10);

    color:
        white;
}


/* ánh sáng góc card */

.result-card::before {

    content: "";

    position: absolute;

    width: 230px;

    height: 230px;

    right: -85px;

    top: -90px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(71,255,213,0.34),
            rgba(71,255,213,0)
            68%
        );
}


/* ánh sáng phụ */

.result-card::after {

    content: "";

    position: absolute;

    width: 160px;

    height: 160px;

    left: -90px;

    bottom: -100px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(0,107,255,0.35),
            transparent 70%
        );
}


.result-type {

    position: relative;

    z-index: 2;

    font-size: 13px;

    font-weight: 850;

    letter-spacing: 1.3px;

    color:
        rgba(255,255,255,0.72);
}


.result-label {

    position: relative;

    z-index: 2;

    margin-top: 25px;

    font-size: 14px;

    color:
        rgba(255,255,255,0.68);
}


.result-interest {

    position: relative;

    z-index: 2;

    margin-top: 4px;

    color:
        white;

    font-size: 29px;

    font-weight: 850;

    letter-spacing: -0.6px;

    font-variant-numeric:
        tabular-nums;
}


.result-total {

    position: relative;

    z-index: 2;

    margin-top: 4px;

    color:
        #65FFDA;

    font-size: 34px;

    font-weight: 900;

    letter-spacing: -1px;

    font-variant-numeric:
        tabular-nums;
}


/* ========================================================
   BADGE
======================================================== */

.profit-badge {

    position: relative;

    z-index: 2;

    display: inline-block;

    margin-top: 18px;

    padding:
        8px 13px;

    border-radius:
        999px;

    background:
        rgba(101,255,218,0.13);

    border:
        1px solid
        rgba(101,255,218,0.28);

    color:
        #72FFDE;

    font-size:
        13px;

    font-weight:
        800;
}


/* ========================================================
   SUMMARY CARD
======================================================== */

.summary-box {

    margin-top: 24px;

    padding: 22px 24px;

    border-radius: 19px;

    background:
        linear-gradient(
            120deg,
            #E3FFF7,
            #EDF8FF
        );

    border:
        1px solid
        #C7EFE4;

    box-shadow:
        0 12px 30px
        rgba(0,179,137,0.08);
}


.summary-label {

    color:
        #23806C;

    font-size:
        14px;

    font-weight:
        750;
}


.summary-money {

    margin-top:
        4px;

    color:
        #075848;

    font-size:
        26px;

    font-weight:
        900;
}


.summary-description {

    margin-top:
        5px;

    color:
        #648177;

    font-size:
        14px;
}


/* ========================================================
   HISTORY
======================================================== */

.history-heading {

    margin-top:
        48px;

    font-size:
        31px;

    font-weight:
        900;

    color:
        #071C35;
}


.history-card {

    margin-top:
        14px;

    padding:
        20px 22px;

    background:
        rgba(
            255,
            255,
            255,
            0.94
        );

    border:
        1px solid
        #DFE8F1;

    border-radius:
        19px;

    box-shadow:
        0 10px 28px
        rgba(13,41,75,0.06);
}


.history-date {

    color:
        #8592A4;

    font-size:
        12px;

    font-weight:
        700;
}


.history-total {

    margin-top:
        5px;

    color:
        #071C35;

    font-size:
        22px;

    font-weight:
        900;
}


.history-detail {

    margin-top:
        8px;

    color:
        #64748B;

    font-size:
        14px;

    line-height:
        1.6;
}


.history-profit {

    color:
        #009976;

    font-weight:
        800;
}


/* ========================================================
   EXPANDER
======================================================== */

div[data-testid="stExpander"] {

    background:
        rgba(
            255,
            255,
            255,
            0.92
        ) !important;

    border:
        1px solid
        #DFE7F0 !important;

    border-radius:
        17px !important;

    overflow:
        hidden;

    color:
        #0A1B33 !important;
}


div[data-testid="stExpander"]
summary {

    color:
        #0A1B33 !important;

    font-weight:
        750 !important;
}


/* ========================================================
   DATAFRAME
======================================================== */

div[data-testid="stDataFrame"] {

    border-radius:
        16px;

    overflow:
        hidden;
}


/* ========================================================
   SECONDARY BUTTON
======================================================== */

div[data-testid="stButton"] button {

    border-radius:
        12px;

    font-weight:
        700;
}


/* ========================================================
   MOBILE
======================================================== */

@media (
    max-width: 768px
) {

    .block-container {

        max-width:
            100% !important;

        padding:
            1.25rem
            1rem
            4rem
            1rem !important;
    }


    .main-header {

        padding-bottom:
            20px;
    }


    .main-title {

        font-size:
            32px !important;

        letter-spacing:
            -1.2px !important;

        line-height:
            1.15;
    }


    .subtitle {

        font-size:
            14px;

        line-height:
            1.5;
    }


    div[data-testid="stForm"] {

        padding:
            20px !important;

        border-radius:
            22px !important;
    }


    div[data-testid="stNumberInput"]
    input {

        min-height:
            50px !important;

        font-size:
            16px !important;
    }


    .result-heading {

        font-size:
            28px;

        margin-top:
            32px;
    }


    .result-card {

        min-height:
            255px;

        padding:
            23px;

        border-radius:
            22px;
    }


    .result-interest {

        font-size:
            24px;
    }


    .result-total {

        font-size:
            27px;

        overflow-wrap:
            anywhere;
    }


    .summary-money {

        font-size:
            23px;
    }


    .history-heading {

        font-size:
            27px;
    }


    .history-total {

        font-size:
            20px;
    }

}


/* ========================================================
   FIX DARK MODE CỦA STREAMLIT
======================================================== */

@media (
    prefers-color-scheme: dark
) {

    .stApp {

        background:
            radial-gradient(
                circle at 8% 8%,
                rgba(0,107,255,.16),
                transparent 28%
            ),
            radial-gradient(
                circle at 92% 10%,
                rgba(0,179,137,.16),
                transparent 28%
            ),
            #F4F8FC !important;

        color:
            #0A1B33 !important;
    }


    div[data-testid="stForm"] {

        background:
            rgba(
                255,
                255,
                255,
                0.95
            ) !important;

        color:
            #0A1B33 !important;
    }


    div[data-testid="stNumberInput"]
    input {

        background:
            #F4F7FB !important;

        color:
            #0A1B33 !important;

        -webkit-text-fill-color:
            #0A1B33 !important;
    }


    div[data-testid="stNumberInput"]
    button {

        background:
            #F4F7FB !important;

        color:
            #0A1B33 !important;
    }


    div[data-testid="stNumberInput"]
    label,
    div[data-testid="stSlider"]
    label {

        color:
            #0A1B33 !important;
    }

}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="main-title">
        Tiết kiệm <span class="gradient-text">thông minh</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style="
        margin-top: 8px;
        margin-bottom: 28px;
        color: #6E7C91;
        font-size: 16px;
        font-weight: 500;
    ">
        Tính toán và so sánh lợi nhuận tiền gửi của bạn.
    </p>
    """,
    unsafe_allow_html=True
)


# =========================================================
# FORM
# =========================================================

with st.form(
    "saving_form"
):

    st.markdown(
        "## Thông tin tiền gửi"
    )

    st.caption(
        "Nhập thông tin khoản tiết kiệm bạn muốn tính."
    )

    col1, col2 = st.columns(
        2,
        gap="large"
    )

    # -------------------------
    # SỐ TIỀN
    # -------------------------

    with col1:

        so_tien = st.number_input(
            "Số tiền gửi (VNĐ)",
            min_value=0,
            value=100_000_000,
            step=1_000_000,
            format="%d"
        )

        st.caption(
            "Số tiền hiện tại: "
            + format_money(
                so_tien
            )
        )


    # -------------------------
    # LÃI SUẤT
    # -------------------------

    with col2:

        lai_suat = st.number_input(
            "Lãi suất (%/năm)",
            min_value=0.0,
            max_value=100.0,
            value=5.90,
            step=0.10,
            format="%.2f"
        )

        st.caption(
            f"Lãi suất hiện tại: "
            f"{lai_suat:.2f}%/năm"
        )


    st.write("")


    # -------------------------
    # KỲ HẠN
    # -------------------------

    so_thang = st.slider(
        "Kỳ hạn gửi",
        min_value=1,
        max_value=36,
        value=12,
        step=1
    )

    st.caption(
        f"Kỳ hạn hiện tại: "
        f"{so_thang} tháng"
    )


    st.write("")


    # -------------------------
    # SUBMIT
    # -------------------------

    submit = (
        st.form_submit_button(
            "Tính tiền tiết kiệm",
            use_container_width=True
        )
    )


# =========================================================
# XỬ LÝ SUBMIT
# =========================================================

if submit:

    if so_tien <= 0:

        st.error(
            "Số tiền gửi phải lớn hơn 0."
        )

    elif lai_suat < 0:

        st.error(
            "Lãi suất không được âm."
        )

    else:

        result = calculate(
            so_tien,
            so_thang,
            lai_suat
        )

        st.session_state.result = (
            result
        )

        # Thêm vào đầu lịch sử
        st.session_state.history.insert(
            0,
            result.copy()
        )

        # Chỉ giữ 10 lần gần nhất
        st.session_state.history = (
            st.session_state.history[:10]
        )


# =========================================================
# KẾT QUẢ
# =========================================================

if st.session_state.result:

    r = (
        st.session_state.result
    )

    st.markdown(
        '<div class="result-heading">'
        'Kết quả'
        '</div>',
        unsafe_allow_html=True
    )


    result_col1, result_col2 = (
        st.columns(
            2,
            gap="large"
        )
    )


    # =====================================================
    # LÃI ĐƠN
    # =====================================================

    with result_col1:

        simple_html = (
            '<div class="result-card">'
            '<div class="result-type">'
            'LÃI ĐƠN'
            '</div>'
            '<div class="result-label">'
            'Tiền lãi nhận được'
            '</div>'
            '<div class="result-interest">'
            + format_money(
                r["simple_interest"]
            )
            + '</div>'
            '<div class="result-label">'
            'Tổng số tiền nhận được'
            '</div>'
            '<div class="result-total">'
            + format_money(
                r["simple_total"]
            )
            + '</div>'
            '</div>'
        )

        st.markdown(
            simple_html,
            unsafe_allow_html=True
        )


    # =====================================================
    # LÃI KÉP
    # =====================================================

    with result_col2:

        compound_html = (
            '<div class="result-card">'
            '<div class="result-type">'
            'LÃI KÉP • GỘP THÁNG'
            '</div>'
            '<div class="result-label">'
            'Tiền lãi nhận được'
            '</div>'
            '<div class="result-interest">'
            + format_money(
                r["compound_interest"]
            )
            + '</div>'
            '<div class="result-label">'
            'Tổng số tiền nhận được'
            '</div>'
            '<div class="result-total">'
            + format_money(
                r["compound_total"]
            )
            + '</div>'
            '<div class="profit-badge">'
            '+ '
            + format_money(
                r["difference"]
            )
            + ' so với lãi đơn'
            '</div>'
            '</div>'
        )

        st.markdown(
            compound_html,
            unsafe_allow_html=True
        )


    # =====================================================
    # CHÊNH LỆCH
    # =====================================================

    summary_html = (
        '<div class="summary-box">'
        '<div class="summary-label">'
        'Lãi kép giúp bạn nhận thêm'
        '</div>'
        '<div class="summary-money">'
        + format_money(
            r["difference"]
        )
        + '</div>'
        '<div class="summary-description">'
        'So với lãi đơn trong cùng kỳ hạn '
        'và cùng mức lãi suất.'
        '</div>'
        '</div>'
    )

    st.markdown(
        summary_html,
        unsafe_allow_html=True
    )


    # =====================================================
    # BẢNG TỔNG KẾT
    # =====================================================

    st.markdown(
        "### Tổng kết kết quả"
    )

    summary_data = {

        "Phương thức": [
            "Lãi đơn",
            "Lãi kép"
        ],

        "Tiền gốc": [
            format_money(
                r["principal"]
            ),
            format_money(
                r["principal"]
            )
        ],

        "Tiền lãi": [
            format_money(
                r["simple_interest"]
            ),
            format_money(
                r["compound_interest"]
            )
        ],

        "Tổng nhận": [
            format_money(
                r["simple_total"]
            ),
            format_money(
                r["compound_total"]
            )
        ]
    }

    st.dataframe(
        summary_data,
        hide_index=True,
        use_container_width=True
    )


    # =====================================================
    # CÔNG THỨC
    # =====================================================

    with st.expander(
        "Xem chi tiết cách tính"
    ):

        # -------------------------
        # LÃI ĐƠN
        # -------------------------

        st.markdown(
            "### Lãi đơn"
        )

        st.latex(
            r"A = P(1 + rt)"
        )

        st.write(
            f"""
**Tiền gốc P:** {format_money(r["principal"])}

**Lãi suất năm r:** {r["annual_rate"]:.4f}

**Thời gian t:** {r["months"]}/12 = {r["years"]:.2f} năm
"""
        )

        st.code(
            f'A = '
            f'{r["principal"]:,.0f} '
            f'× '
            f'(1 + '
            f'{r["annual_rate"]:.4f} '
            f'× '
            f'{r["years"]:.2f})'
        )

        st.success(
            "Tổng tiền lãi đơn: "
            + format_money(
                r["simple_total"]
            )
        )

        st.divider()


        # -------------------------
        # LÃI KÉP
        # -------------------------

        st.markdown(
            "### Lãi kép"
        )

        st.latex(
            r"A = P(1+r/12)^n"
        )

        st.write(
            f"""
**Tiền gốc P:** {format_money(r["principal"])}

**Lãi suất năm r:** {r["annual_rate"]:.4f}

**Số tháng n:** {r["months"]}

**Lãi suất tháng:** {r["monthly_rate"] * 100:.4f}%
"""
        )

        st.code(
            f'A = '
            f'{r["principal"]:,.0f} '
            f'× '
            f'(1 + '
            f'{r["monthly_rate"]:.6f})'
            f'^{r["months"]}'
        )

        st.success(
            "Tổng tiền lãi kép: "
            + format_money(
                r["compound_total"]
            )
        )


# =========================================================
# LỊCH SỬ TRA CỨU
# =========================================================

st.markdown(
    '<div class="history-heading">'
    'Lịch sử tra cứu'
    '</div>',
    unsafe_allow_html=True
)

st.caption(
    "Các phép tính gần đây trong phiên làm việc."
)


# =========================================================
# CÓ LỊCH SỬ
# =========================================================

if st.session_state.history:

    title_col, delete_col = (
        st.columns(
            [4, 1]
        )
    )

    with delete_col:

        if st.button(
            "Xóa lịch sử",
            use_container_width=True
        ):

            st.session_state.history = []

            st.rerun()


    for item in (
        st.session_state.history
    ):

        history_html = (
            '<div class="history-card">'
            '<div class="history-date">'
            + item["time"]
            + '</div>'
            '<div class="history-total">'
            + format_money(
                item["compound_total"]
            )
            + '</div>'
            '<div class="history-detail">'
            'Tiền gửi: <b>'
            + format_money(
                item["principal"]
            )
            + '</b>'
            '<br>'
            'Kỳ hạn: <b>'
            + str(
                item["months"]
            )
            + ' tháng</b>'
            ' &nbsp; • &nbsp; '
            'Lãi suất: <b>'
            + f'{item["rate"]:.2f}%/năm'
            + '</b>'
            '<br>'
            'Lãi kép nhận được: '
            '<span class="history-profit">'
            + format_money(
                item["compound_interest"]
            )
            + '</span>'
            '</div>'
            '</div>'
        )

        st.markdown(
            history_html,
            unsafe_allow_html=True
        )


# =========================================================
# CHƯA CÓ LỊCH SỬ
# =========================================================

else:

    st.info(
        "Chưa có lịch sử tra cứu. "
        "Hãy thực hiện phép tính đầu tiên."
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    "<br>",
    unsafe_allow_html=True
)

st.divider()

st.caption(
    "Số liệu chỉ mang tính chất tham khảo, "
    "không phải cam kết lãi suất thực tế."
)
