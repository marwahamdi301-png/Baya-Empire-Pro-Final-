import streamlit as st


def setup_style():
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');

            * {
                font-family: 'Cairo', sans-serif;
            }

            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(0, 242, 255, 0.10), transparent 30%),
                    radial-gradient(circle at bottom right, rgba(255, 0, 85, 0.10), transparent 30%),
                    #070b14;
                color: white;
            }

            .block-container {
                padding-top: 1.5rem;
                padding-bottom: 2.5rem;
            }

            .hero {
                background: linear-gradient(135deg, rgba(0,242,255,0.12), rgba(255,0,85,0.08));
                border: 1px solid rgba(0,242,255,0.25);
                border-radius: 24px;
                padding: 28px;
                margin-bottom: 22px;
                text-align: center;
                box-shadow: 0 0 35px rgba(0,242,255,0.08);
            }

            .hero h1 {
                color: #00f2ff;
                font-size: 44px;
                font-weight: 900;
                margin-bottom: 8px;
            }

            .hero p {
                color: #aab3c5;
                font-size: 17px;
                margin: 0;
            }

            .metric-card {
                background: rgba(255, 255, 255, 0.045);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 18px;
                padding: 20px;
                min-height: 120px;
                box-shadow: 0 8px 28px rgba(0,0,0,0.22);
            }

            .metric-label {
                color: #aab3c5;
                font-size: 14px;
                margin-bottom: 8px;
            }

            .metric-value {
                font-size: 28px;
                font-weight: 900;
                margin-bottom: 4px;
            }

            .metric-note {
                color: #7f8aa6;
                font-size: 12px;
            }

            .signal-buy {
                color: #00ff88;
                font-weight: 900;
            }

            .signal-sell {
                color: #ff0055;
                font-weight: 900;
            }

            .signal-hold {
                color: #ffaa00;
                font-weight: 900;
            }

            .footer {
                text-align: center;
                opacity: 0.45;
                font-size: 13px;
                margin-top: 35px;
            }

            .impact-card {
                background: rgba(255,255,255,0.045);
                border: 1px solid rgba(0,242,255,0.18);
                border-radius: 18px;
                padding: 20px;
                margin-bottom: 12px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )


def page_header(title, subtitle):
    st.markdown(
        f"""
        <div class="hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def metric_card(label, value, note="", color="#ffffff"):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value" style="color:{color};">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def risk_notice():
    st.warning(
        "تنبيه مهم: البيانات والإشارات داخل المنصة تعليمية وتجريبية فقط. "
        "ليست نصيحة مالية أو استثمارية، ولا توجد أرباح مضمونة."
    )


def footer():
    st.markdown(
        """
        <div class="footer">
            🛡️ Baya Empire Pro 2026 — Paper Trading / AI Signals / Africa Impact<br>
            Technology for African Impact
        </div>
        """,
        unsafe_allow_html=True
    )
