import streamlit as st

st.set_page_config(
    page_title="Baya Empire Pro",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

from src.ui import setup_style, page_header, metric_card, risk_notice, footer

setup_style()

page_header(
    "🛡️ BAYA EMPIRE PRO",
    "منصة تداول تجريبي، إشارات AI، مؤشرات فنية، ومحفظة افتراضية لدعم رؤية مشاريع أفريقية"
)

risk_notice()

c1, c2, c3 = st.columns(3)

with c1:
    metric_card(
        "📈 Market",
        "Live Charts",
        "شموع + RSI + MA + MACD",
        "#00f2ff"
    )

with c2:
    metric_card(
        "🤖 AI Signals",
        "Smart Signals",
        "إشارات تعليمية مبنية على مؤشرات فنية",
        "#ffaa00"
    )

with c3:
    metric_card(
        "💼 Portfolio",
        "Paper Trading",
        "محفظة افتراضية بدون تداول حقيقي",
        "#00ff88"
    )

st.markdown("## 🌍 رؤية Baya Empire Impact")

st.markdown(
    """
    Baya Empire ليست فقط لوحة أسعار. الهدف هو بناء منصة رقمية تجمع بين:
    
    - التعليم المالي والتقني.
    - محفظة افتراضية للتجربة والتعلم.
    - إشارات ذكية تعليمية.
    - مجتمع يدعم مشاريع تنموية في أفريقيا.
    - شفافية في عرض المشاريع والنتائج.
    
    استخدم القائمة الجانبية للانتقال بين الصفحات.
    """
)

st.markdown("## 🧭 الصفحات المتوفرة")

st.markdown(
    """
    - **Market**: شارتات حية مع RSI و SMA و EMA و MACD.
    - **AI Signals**: إشارات تعليمية مبنية على تحليل فني.
    - **Portfolio**: محفظة افتراضية، رصيد، مراكز، PnL، وسجل عمليات.
    - **Africa Impact**: رؤية المشروع ودعم المبادرات الأفريقية.
    """
)

footer()
