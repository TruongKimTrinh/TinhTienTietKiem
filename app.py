import streamlit as st
from datetime import datetime

# =========================================================
# CẤU HÌNH TRANG
# =========================================================
st.set_page_config(
    page_title="Tiết kiệm có kỳ hạn",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# =========================================================
# HÀM FORMAT TIỀN
# =========================================================
def format_money(value):
    try:
        return f"{float(value):,.0f}".replace(",", ".")
    except:
        return "0"


# =========================================================
# HÀM TÍNH LÃI
# =========================================================
def tinh_lai(so_tien, so_thang, lai_suat):

    r_nam = lai_suat / 100
    so_nam = so_thang / 12

    # -------------------------
    # LÃI ĐƠN
    # -------------------------
    lai_don = so_tien * r_nam * so_nam

    tong_lai_don = (
        so_tien + lai_don
    )

    # -------------------------
    # LÃI KÉP
    # -------------------------
    r_thang = r_nam / 12

    tong_lai_kep = (
        so_tien
        * (1 + r_thang) ** so_thang
    )

    lai_kep = (
        tong_lai_kep - so_tien
    )

    return {
        "lai_don": lai_don,
        "tong_lai_don": tong_lai_don,
        "lai_kep": lai_kep,
        "tong_lai_kep": tong_lai_kep
    }


# =========================================================
# SESSION STATE
# =========================================================
if "history" not in st.session_state:
    st.session_state.history = []

if "result" not in st.session_state:
    st.session_state.result = None

if "money_text" not in st.session_state:
    st.session_state.money_text = "100000000"


# =========================================================
# CSS
# =========================================================
st.markdown("""
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap'
);

* {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.stApp {

    background:

        radial-gradient(
            circle at 10% 0%,
            rgba(37,99,235,.10),
            transparent 30%
        ),

        radial-gradient(
            circle at 100% 10%,
            rgba(0,184,148,.10),
            transparent 30%
        ),

        #F2F7FB;
}


/* ============================
   KHUNG CHÍNH
============================ */

.block-container {

    width: 100%;

    max-width: 760px;

    padding-top: 35px;

    padding-left: 28px;

    padding-right: 28px;

    padding-bottom: 60px;
}


#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent;
}


/* ============================
   TIÊU ĐỀ
============================ */

h1 {

    color: #102A43 !important;

    font-size: 30px !important;

    font-weight: 800 !important;

    letter-spacing: -1px !important;
}


h2 {

    color: #102A43 !important;

    font-size: 23px !important;

    font-weight: 800 !important;

    letter-spacing: -.5px !important;
}


h3 {

    color: #102A43 !important;

    font-weight: 800 !important;
}


/* ============================
   CARD
============================ */

div[data-testid="stVerticalBlockBorderWrapper"] {

    background: rgba(255,255,255,.95);

    border: 1px solid #DCE7F1 !important;

    border-radius: 22px;

    box-shadow:
        0 12px 35px rgba(16,42,67,.06);
}


/* ============================
   TEXT INPUT TIỀN
============================ */

div[data-testid="stTextInput"] input {

    min-height: 52px;

    background: #F7FAFC;

    border: 1px solid #DCE7F1;

    border-radius: 14px;

    color: #102A43;

    font-size: 17px;

    font-weight: 700;

    padding-left: 16px;

    transition: all .2s ease;
}


div[data-testid="stTextInput"] input:focus {

    background: #FFFFFF;

    border-color: #00B894;

    box-shadow:
        0 0 0 4px rgba(0,184,148,.11);
}


/* ============================
   LABEL
============================ */

label[data-testid="stWidgetLabel"] p {

    color: #334E68 !important;

    font-weight: 700 !important;
}


/* ============================
   SLIDER
============================ */

div[data-testid="stSlider"] {

    padding-top: 5px;
}


/* ============================
   SEGMENTED CONTROL
============================ */

div[data-testid="stSegmentedControl"] button {

    min-height: 42px;

    border-radius: 12px !important;

    font-weight: 700;
}


/* ============================
   NÚT CHÍNH
============================ */

div[data-testid="stButton"] button[kind="primary"] {

    min-height: 52px;

    border: none;

    border-radius: 15px;

    color: white;

    font-size: 14px;

    font-weight: 800;

    background:
        linear-gradient(
            100deg,
            #00B894,
            #00A67E
        );

    box-shadow:
        0 8px 22px rgba(0,184,148,.20);

    transition: .2s ease;
}


div[data-testid="stButton"] button[kind="primary"]:hover {

    transform: translateY(-1px);

    background:
        linear-gradient(
            100deg,
            #00A984,
            #009873
        );

    box-shadow:
        0 10px 26px rgba(0,184,148,.28);
}


/* ============================
   NÚT PHỤ
============================ */

div[data-testid="stButton"] button[kind="secondary"] {

    min-height: 44px;

    border-radius: 12px;

    border: 1px solid #DCE7F1;

    background: white;

    color: #334E68;

    font-weight: 700;
}


div[data-testid="stButton"] button[kind="secondary"]:hover {

    color: #00A67E;

    border-color: #00B894;

    background: #ECFDF8;
}


/* ============================
   METRIC
============================ */

div[data-testid="stMetric"] {

    background:
        linear-gradient(
            145deg,
            #FFFFFF,
            #F4FAFD
        );

    border: 1px solid #DCE7F1;

    border-radius: 17px;

    padding: 19px;

    box-shadow:
        0 6px 18px rgba(16,42,67,.04);
}


div[data-testid="stMetricLabel"] p {

    color: #627D98 !important;

    font-weight: 600 !important;
}


div[data-testid="stMetricValue"] {

    color: #102A43 !important;

    font-weight: 800 !important;

    font-variant-numeric: tabular-nums;
}


/* ============================
   ALERT
============================ */

div[data-testid="stAlert"] {

    border-radius: 15px;
}


/* ============================
   EXPANDER
============================ */

div[data-testid="stExpander"] {

    background: white;

    border: 1px solid #DCE7F1;

    border-radius: 17px;

    overflow: hidden;

    box-shadow:
        0 6px 20px rgba(16,42,67,.04);
}


/* ============================
   DIVIDER
============================ */

hr {

    border-color: #DCE7F1 !important;
}


/* ============================
   MOBILE
============================ */

@media (max-width: 600px) {

    .block-container {

        max-width: 430px;

        padding-top: 22px;

        padding-left: 15px;

        padding-right: 15px;

        padding-bottom: 40px;
    }

    h1 {
        font-size: 25px !important;
    }

    h2 {
        font-size: 20px !important;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================
st.title("Tiết kiệm có kỳ hạn")

st.caption(
    "Tính toán và so sánh lợi nhuận tiền gửi của bạn."
)


# =========================================================
# FORM NHẬP
# =========================================================
with st.container(border=True):

    st.subheader("Thông tin tiền gửi")

    st.caption(
        "Nhập thông tin khoản tiết kiệm bạn muốn tính."
    )


        # =====================================================
    # SỐ TIỀN GỬI
    # =====================================================

    # Lấy giá trị hiện tại từ session
    money_text = st.session_state.get("money_text", "100000000")

    # Chuyển sang số để hiển thị
    try:
        clean_money = (
            str(money_text)
            .replace(".", "")
            .replace(",", "")
            .replace(" ", "")
        )

        current_money = int(clean_money) if clean_money else 0

    except (ValueError, TypeError):
        current_money = 0


    # =====================================================
    # LABEL + SỐ TIỀN HIỆN TẠI
    # =====================================================
    col_label, col_value = st.columns(
        [1.1, 1],
        vertical_alignment="center"
    )

    with col_label:
        st.markdown(
            """
            <div style="
                color:#334E68;
                font-size:14px;
                font-weight:800;
                padding-bottom:4px;
            ">
                Số tiền gửi (VNĐ)
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_value:

        if current_money > 0:
            st.markdown(
                f"""
                <div style="
                    text-align:right;
                    color:#00A67E;
                    font-size:16px;
                    font-weight:800;
                    padding-bottom:4px;
                    font-variant-numeric:tabular-nums;
                ">
                    {format_money(current_money)} đ
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div style="
                    text-align:right;
                    color:#E5484D;
                    font-size:13px;
                    font-weight:700;
                    padding-bottom:4px;
                ">
                    Chưa hợp lệ
                </div>
                """,
                unsafe_allow_html=True
            )


    # =====================================================
    # Ô NHẬP TIỀN
    # =====================================================
    money_text = st.text_input(
        "Số tiền",
        key="money_text",
        label_visibility="collapsed",
        placeholder="Ví dụ: 100000000"
    )


    # =====================================================
    # CHUYỂN GIÁ TRỊ INPUT THÀNH SỐ
    # =====================================================
    try:
        clean_money = (
            str(money_text)
            .replace(".", "")
            .replace(",", "")
            .replace(" ", "")
        )

        so_tien = int(clean_money) if clean_money else 0

    except (ValueError, TypeError):
        so_tien = 0


    # =====================================================
    # VALIDATE
    # =====================================================
    if money_text and so_tien <= 0:
        st.error("Vui lòng nhập số tiền hợp lệ.")

    elif money_text and not clean_money.isdigit():
        st.error("Số tiền chỉ được chứa chữ số.")


    st.write("")


    # =====================================================
    # KỲ HẠN
    # =====================================================
    so_thang = st.slider(
        "Kỳ hạn gửi",
        min_value=1,
        max_value=36,
        value=12,
        step=1
    )


    st.caption(
        f"Kỳ hạn hiện tại: "
        f"**{so_thang} tháng**"
    )


    st.write("")


    # =====================================================
    # LÃI SUẤT
    # =====================================================
    lai_suat = st.slider(
        "Lãi suất (%/năm)",
        min_value=0.0,
        max_value=12.0,
        value=6.0,
        step=0.1
    )


    st.caption(
        f"Lãi suất hiện tại: "
        f"**{lai_suat:.1f}%/năm**"
    )


    st.write("")


    # =====================================================
    # HÌNH THỨC
    # =====================================================
    loai_lai = st.segmented_control(
        "Hình thức tính",
        options=[
            "Lãi kép",
            "Lãi đơn"
        ],
        default="Lãi kép"
    )


    st.write("")


    # =====================================================
    # SUBMIT
    # =====================================================
    submit = st.button(
        "Tính tiền tiết kiệm",
        type="primary",
        use_container_width=True
    )


# =========================================================
# XỬ LÝ SUBMIT
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

        data = tinh_lai(
            so_tien,
            so_thang,
            lai_suat
        )


        # =================================================
        # CHỌN KẾT QUẢ
        # =================================================
        if loai_lai == "Lãi đơn":

            tong_nhan = (
                data["tong_lai_don"]
            )

            tien_lai = (
                data["lai_don"]
            )

        else:

            tong_nhan = (
                data["tong_lai_kep"]
            )

            tien_lai = (
                data["lai_kep"]
            )


        # =================================================
        # TẠO RESULT
        # =================================================
        result = {

            "so_tien":
                so_tien,

            "so_thang":
                so_thang,

            "lai_suat":
                lai_suat,

            "loai_lai":
                loai_lai,

            "tong_nhan":
                tong_nhan,

            "tien_lai":
                tien_lai,

            "lai_don":
                data["lai_don"],

            "tong_lai_don":
                data["tong_lai_don"],

            "lai_kep":
                data["lai_kep"],

            "tong_lai_kep":
                data["tong_lai_kep"],

            "time":
                datetime.now().strftime(
                    "%H:%M - %d/%m/%Y"
                )
        }


        # =================================================
        # LƯU RESULT
        # =================================================
        st.session_state.result = result


        # =================================================
        # LƯU HISTORY
        # =================================================
        st.session_state.history.insert(
            0,
            result.copy()
        )


        # CHỈ GIỮ 10 LẦN
        st.session_state.history = (
            st.session_state.history[:10]
        )


# =========================================================
# KẾT QUẢ
# =========================================================
if st.session_state.result is not None:

    kq = st.session_state.result


    st.write("")
    st.write("")

    st.subheader("Kết quả")

    st.caption(
        "Kết quả dựa trên thông tin bạn vừa nhập."
    )


    # =====================================================
    # HERO KẾT QUẢ
    # =====================================================
    with st.container(border=True):

        st.caption(
            "SỐ TIỀN DỰ KIẾN NHẬN"
        )

        st.markdown(
            f"""
            # {format_money(kq['tong_nhan'])} đ
            """
        )

        st.caption(
            f"{kq['loai_lai']}  •  "
            f"{kq['so_thang']} tháng  •  "
            f"{kq['lai_suat']:.1f}%/năm"
        )


    st.write("")


    # =====================================================
    # THÔNG TIN KẾT QUẢ
    # =====================================================
    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Số tiền ban đầu",
            f"{format_money(kq['so_tien'])} đ"
        )


    with col2:

        st.metric(
            "Tiền lãi nhận được",
            f"+{format_money(kq['tien_lai'])} đ"
        )


    st.write("")


    # =====================================================
    # SO SÁNH
    # =====================================================
    st.subheader(
        "So sánh hình thức"
    )


    col1, col2 = st.columns(2)


    # -----------------------------------------------------
    # LÃI ĐƠN
    # -----------------------------------------------------
    with col1:

        with st.container(border=True):

            st.caption(
                "LÃI ĐƠN"
            )

            st.markdown(
                f"""
                ### {format_money(kq['tong_lai_don'])} đ
                """
            )

            st.write(
                "Tiền lãi:"
            )

            st.markdown(
                f"""
                **+{format_money(kq['lai_don'])} đ**
                """
            )


    # -----------------------------------------------------
    # LÃI KÉP
    # -----------------------------------------------------
    with col2:

        with st.container(border=True):

            st.caption(
                "LÃI KÉP"
            )

            st.markdown(
                f"""
                ### {format_money(kq['tong_lai_kep'])} đ
                """
            )

            st.write(
                "Tiền lãi:"
            )

            st.markdown(
                f"""
                **+{format_money(kq['lai_kep'])} đ**
                """
            )


    # =====================================================
    # CHÊNH LỆCH
    # =====================================================
    chenh_lech = (
        kq["tong_lai_kep"]
        -
        kq["tong_lai_don"]
    )


    if chenh_lech > 0:

        st.success(
            f"📈 Lãi kép giúp bạn nhận thêm "
            f"**{format_money(chenh_lech)} đ** "
            f"so với lãi đơn."
        )

    elif chenh_lech == 0:

        st.info(
            "Hai hình thức đang cho cùng kết quả."
        )

    else:

        st.info(
            f"Lãi đơn cao hơn "
            f"**{format_money(abs(chenh_lech))} đ**."
        )


    # =====================================================
    # CÔNG THỨC
    # =====================================================
    with st.expander(
        "Xem chi tiết cách tính",
        expanded=False
    ):

        P = kq["so_tien"]

        n = kq["so_thang"]

        r = (
            kq["lai_suat"]
            / 100
        )

        t = (
            n / 12
        )


        # =================================================
        # LÃI ĐƠN
        # =================================================
        st.markdown(
            "### Lãi đơn"
        )

        st.latex(
            r"A = P(1 + r \times t)"
        )

        st.write(
            f"Số tiền gửi P: "
            f"**{format_money(P)} đ**"
        )

        st.write(
            f"Lãi suất r: "
            f"**{r:.4f}**"
        )

        st.write(
            f"Thời gian t: "
            f"**{n}/12 = {t:.2f} năm**"
        )


        st.code(
            f"A = {format_money(P)} × "
            f"(1 + {r:.4f} × {t:.2f})"
        )


        st.success(
            f"Tổng nhận: "
            f"{format_money(kq['tong_lai_don'])} đ"
        )


        st.divider()


        # =================================================
        # LÃI KÉP
        # =================================================
        st.markdown(
            "### Lãi kép"
        )

        st.latex(
            r"A = P(1 + r/12)^n"
        )

        st.write(
            f"Số tiền gửi P: "
            f"**{format_money(P)} đ**"
        )

        st.write(
            f"Lãi suất năm r: "
            f"**{r:.4f}**"
        )

        st.write(
            f"Số kỳ n: "
            f"**{n} tháng**"
        )


        st.code(
            f"A = {format_money(P)} × "
            f"(1 + {r:.4f}/12)^{n}"
        )


        st.success(
            f"Tổng nhận: "
            f"{format_money(kq['tong_lai_kep'])} đ"
        )


# =========================================================
# LỊCH SỬ
# =========================================================
st.write("")
st.write("")

st.divider()


history_title, history_delete = st.columns(
    [3, 1],
    vertical_alignment="center"
)


with history_title:

    st.subheader(
        "Lịch sử tra cứu"
    )

    st.caption(
        "Các phép tính gần đây trong phiên làm việc."
    )


with history_delete:

    if st.session_state.history:

        if st.button(
            "Xóa lịch sử",
            use_container_width=True
        ):

            st.session_state.history = []

            st.session_state.result = None

            st.rerun()


# =========================================================
# CHƯA CÓ LỊCH SỬ
# =========================================================
if not st.session_state.history:

    st.info(
        "Chưa có lịch sử tính toán."
    )


# =========================================================
# HIỂN THỊ LỊCH SỬ
# =========================================================
else:

    for index, item in enumerate(
        st.session_state.history,
        start=1
    ):

        with st.container(border=True):

            # =================================================
            # HEADER HISTORY
            # =================================================
            c1, c2 = st.columns(
                [2, 1]
            )


            with c1:

                st.markdown(
                    f"""
                    ### {format_money(item['tong_nhan'])} đ
                    """
                )

                st.caption(
                    f"Lần tính #{index}"
                )


            with c2:

                st.caption(
                    item["time"]
                )


            st.divider()


            # =================================================
            # CHI TIẾT
            # =================================================
            c1, c2, c3 = st.columns(3)


            with c1:

                st.caption(
                    "Số tiền gửi"
                )

                st.markdown(
                    f"""
                    **{format_money(item['so_tien'])} đ**
                    """
                )


            with c2:

                st.caption(
                    "Kỳ hạn"
                )

                st.markdown(
                    f"""
                    **{item['so_thang']} tháng**
                    """
                )


            with c3:

                st.caption(
                    "Lãi suất"
                )

                st.markdown(
                    f"""
                    **{item['lai_suat']:.1f}%/năm**
                    """
                )


            c4, c5 = st.columns(2)


            with c4:

                st.caption(
                    "Hình thức"
                )

                st.markdown(
                    f"""
                    **{item['loai_lai']}**
                    """
                )


            with c5:

                st.caption(
                    "Tiền lãi"
                )

                st.markdown(
                    f"""
                    **+{format_money(item['tien_lai'])} đ**
                    """
                )


# =========================================================
# FOOTER
# =========================================================
st.write("")

st.divider()

st.caption(
    "Số liệu chỉ mang tính chất tham khảo, "
    "không phải cam kết lãi suất thực tế."
)