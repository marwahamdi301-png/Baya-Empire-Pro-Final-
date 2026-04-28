import streamlit as st

# 1. إعداد الصفحة (يجب أن يكون أول سطر برمي)
st.set_page_config(
    page_title="Baya Empire Pro | Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# محاولة استدعاء مكتبة التحديث التلقائي
try:
    from streamlit_autorefresh import st_autorefresh
except ImportError:
    st_autorefresh = None

# استدعاء أدوات الإمبراطورية من مجلد src
from src.config import DATA_SOURCES, SYMBOLS, INTERVALS
from src.ui import setup_style, page_header, metric_card, risk_notice, footer
from src.data import get_ticker, get_klines
from src.indicators import add_indicators
from src.charts import make_market_chart

# 2. تفعيل التصميم النيوني
setup_style()

# --- القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.image("https://img.icons8.com/nolan/128/shield.png", width=100)
    st.markdown("## 🧭 إعدادات السوق")
    
    data_source = st.selectbox("مصدر البيانات", list(DATA_SOURCES.keys()), index=0)
    base_url = DATA_SOURCES[data_source]
    
    symbol = st.selectbox("زوج التداول", SYMBOLS, index=0)
    interval_label = st.selectbox("الفاصل الزمني", list(INTERVALS.keys()), index=3)
    interval = INTERVALS[interval_label]
    
    refresh_seconds = st.selectbox("تحديث تلقائي", [30, 60, 300], index=0, 
                                    format_func=lambda x: f"كل {x} ثانية")

# تفعيل التحديث التلقائي إذا كان متاحاً
if st_autorefresh:
    st_autorefresh(interval=refresh_seconds * 1000, key="market_refresh")

# --- واجهة الإمبراطورية الرئيسية ---
page_header("🛡️ BAYA EMPIRE PRO", "منصة تداول ذكية ورؤية تنموية لأفريقيا")

# عرض الأقسام بشكل فخم
st.markdown("### 🧭 خارطة الإمبراطورية")
cols = st.columns(2)
with cols[0]:
    st.markdown("""
    - **Market**: تحليل فني حي (مفتوح الآن أدناه).
    - **AI Signals**: توصيات تعليمية ذكية.
    - **Portfolio**: إدارة محفظتك الافتراضية.
    """)
with cols[1]:
    st.markdown("""
    - **Africa Impact**: رؤيتنا لدعم القارة.
    - **Admin**: لوحة التحكم المركزية (محمية).
    - **Whitepaper**: الدليل التقني الشامل.
    """)

st.divider()

# --- محرك السوق (Market Engine) ---
risk_notice()

ticker, error = get_ticker(symbol, base_url)

if ticker:
    change_color = "#00ff88" if ticker["change"] >= 0 else "#ff0055"
    change_arrow = "▲" if ticker["change"] >= 0 else "▼"
    
    # بطاقات المؤشرات السريعة
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("السعر الحالي", f"${ticker['price']:,.2f}", symbol, "#00f2ff")
    with c2:
        metric_card("تغير 24س", f"{change_arrow} {ticker['change']:.2f}%", "24h", change_color)
    with c3:
        metric_card("أعلى سعر", f"${ticker['high']:,.2f}", "24h High", "#ffaa00")
    with c4:
        metric_card("أقل سعر", f"${ticker['low']:,.2f}", "24h Low", "#ff6b6b")

    # جلب البيانات ورسم الشارت
    df, candle_error = get_klines(symbol, interval, 200, base_url)
    if df is not None and not df.empty:
        df = add_indicators(df)
        fig = make_market_chart(df, symbol, interval_label)
        st.plotly_chart(fig, use_container_width=True)
        
        # عرض المؤشرات الفنية أسفل الشارت
        latest = df.iloc[-1]
        m1, m2, m3 = st.columns(3)
        with m1:
            metric_card("RSI 14", f"{latest['RSI14']:.2f}", "Technical Strength", "#00f2ff")
        with m2:
            metric_card("SMA 50", f"${latest['SMA50']:,.2f}", "Trend Line", "#ffaa00")
        with m3:
            metric_card("EMA 21", f"${latest['EMA21']:,.2f}", "Momentum", "#00ff88")
else:
    st.error(f"خطأ في الاتصال بالبيانات: {error}")

footer()
