import streamlit as st

st.set_page_config(
    page_title="Market | Baya Empire",
    page_icon="📈",
    layout="wide"
)

try:
    from streamlit_autorefresh import st_autorefresh
except ImportError:
    st_autorefresh = None

from src.config import DATA_SOURCES, SYMBOLS, INTERVALS
from src.ui import setup_style, page_header, metric_card, risk_notice, footer
from src.data import get_ticker, get_klines
from src.indicators import add_indicators
from src.charts import make_market_chart

setup_style()

with st.sidebar:
    st.markdown("## 📈 Market Settings")

    data_source = st.selectbox(
        "مصدر البيانات",
        list(DATA_SOURCES.keys()),
        index=0
    )

    base_url = DATA_SOURCES[data_source]

    symbol = st.selectbox(
        "زوج التداول",
        SYMBOLS,
        index=0
    )

    interval_label = st.selectbox(
        "الفاصل الزمني",
        list(INTERVALS.keys()),
        index=3
    )

    interval = INTERVALS[interval_label]

    candle_limit = st.slider(
        "عدد الشموع",
        min_value=60,
        max_value=500,
        value=200,
        step=20
    )

    refresh_seconds = st.selectbox(
        "التحديث التلقائي",
        [30, 60, 300],
        index=0,
        format_func=lambda x: f"كل {x} ثانية" if x < 60 else f"كل {x // 60} دقائق"
    )

if st_autorefresh:
    st_autorefresh(
        interval=refresh_seconds * 1000,
        key="market_refresh"
    )

page_header(
    "📈 Market Dashboard",
    "شموع حية + مؤشرات فنية RSI / SMA / EMA / MACD"
)

risk_notice()

ticker, error = get_ticker(symbol, base_url)

if not ticker:
    st.error(f"فشل جلب بيانات السعر: {error}")
    st.stop()

change_color = "#00ff88" if ticker["change"] >= 0 else "#ff0055"
change_arrow = "▲" if ticker["change"] >= 0 else "▼"

c1, c2, c3, c4 = st.columns(4)

with c1:
    metric_card("السعر الحالي", f"${ticker['price']:,.2f}", symbol, "#00f2ff")

with c2:
    metric_card("تغير 24 ساعة", f"{change_arrow} {ticker['change']:.2f}%", "24h", change_color)

with c3:
    metric_card("أعلى سعر", f"${ticker['high']:,.2f}", "24h High", "#ffaa00")

with c4:
    metric_card("أقل سعر", f"${ticker['low']:,.2f}", "24h Low", "#ff6b6b")

st.divider()

df, candle_error = get_klines(
    symbol=symbol,
    interval=interval,
    limit=candle_limit,
    base_url=base_url
)

if candle_error or df is None or df.empty:
    st.warning(f"تعذر تحميل الشارت: {candle_error}")
    st.stop()

df = add_indicators(df)

fig = make_market_chart(df, symbol, interval_label)
st.plotly_chart(fig, use_container_width=True)

latest = df.iloc[-1]

m1, m2, m3, m4 = st.columns(4)

with m1:
    rsi_value = latest.get("RSI14")
    metric_card(
        "RSI 14",
        f"{rsi_value:.2f}" if rsi_value == rsi_value else "N/A",
        "أقل من 30 تشبع بيع، أعلى من 70 تشبع شراء",
        "#00f2ff"
    )

with m2:
    metric_card(
        "SMA20",
        f"${latest['SMA20']:,.2f}" if latest["SMA20"] == latest["SMA20"] else "N/A",
        "متوسط 20 شمعة",
        "#ffaa00"
    )

with m3:
    metric_card(
        "SMA50",
        f"${latest['SMA50']:,.2f}" if latest["SMA50"] == latest["SMA50"] else "N/A",
        "متوسط 50 شمعة",
        "#a855f7"
    )

with m4:
    metric_card(
        "EMA21",
        f"${latest['EMA21']:,.2f}" if latest["EMA21"] == latest["EMA21"] else "N/A",
        "متوسط أسي 21",
        "#00ff88"
    )

footer()
