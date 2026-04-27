import streamlit as st

st.set_page_config(
    page_title="Watchlist & Alerts | Baya Empire",
    page_icon="🔔",
    layout="wide"
)

try:
    from streamlit_autorefresh import st_autorefresh
except ImportError:
    st_autorefresh = None

import pandas as pd

from src.config import DATA_SOURCES, SYMBOLS
from src.ui import setup_style, page_header, metric_card, risk_notice, footer
from src.data import get_ticker
from src.db import (
    init_db,
    add_to_watchlist,
    remove_from_watchlist,
    get_watchlist,
    create_alert,
    get_alerts,
    evaluate_alerts
)

setup_style()
init_db()

with st.sidebar:
    st.markdown("## 🔔 Watchlist Settings")

    data_source = st.selectbox(
        "مصدر البيانات",
        list(DATA_SOURCES.keys()),
        index=0
    )

    base_url = DATA_SOURCES[data_source]

    refresh_seconds = st.selectbox(
        "التحديث التلقائي",
        [30, 60, 300],
        index=0,
        format_func=lambda x: f"كل {x} ثانية" if x < 60 else f"كل {x // 60} دقائق"
    )

if st_autorefresh:
    st_autorefresh(
        interval=refresh_seconds * 1000,
        key="watchlist_refresh"
    )

page_header(
    "🔔 Watchlist & Price Alerts",
    "قائمة متابعة وتنبيهات سعرية تعليمية"
)

risk_notice()

st.markdown("## ⭐ إدارة قائمة المتابعة")

col_add, col_button = st.columns([2, 1])

with col_add:
    selected_symbol = st.selectbox(
        "اختر زوجاً لإضافته",
        SYMBOLS
    )

with col_button:
    st.write("")
    st.write("")
    if st.button("إضافة للقائمة", use_container_width=True):
        add_to_watchlist(selected_symbol)
        st.success(f"تمت إضافة {selected_symbol}.")
        st.rerun()

watchlist = get_watchlist()

if not watchlist:
    st.info("قائمة المتابعة فارغة. أضف زوجاً من الأعلى.")
else:
    st.markdown("### الأزواج في قائمة المتابعة")

    for sym in watchlist:
        c1, c2 = st.columns([4, 1])

        with c1:
            st.write(f"⭐ {sym}")

        with c2:
            if st.button("حذف", key=f"remove_{sym}"):
                remove_from_watchlist(sym)
                st.rerun()

st.divider()

active_alerts = get_alerts(active_only=True)

symbols_to_fetch = set(watchlist)

if not active_alerts.empty:
    for sym in active_alerts["symbol"].unique().tolist():
        symbols_to_fetch.add(sym)

price_rows = []
price_map = {}

for sym in sorted(symbols_to_fetch):
    ticker, error = get_ticker(sym, base_url)

    if ticker:
        price_map[sym] = ticker["price"]

        price_rows.append(
            {
                "الزوج": sym,
                "السعر": ticker["price"],
                "تغير 24h": ticker["change"],
                "الأعلى": ticker["high"],
                "الأدنى": ticker["low"],
            }
        )

triggered_alerts = evaluate_alerts(price_map)

if triggered_alerts:
    st.success("تم تفعيل تنبيهات سعرية:")

    for alert in triggered_alerts:
        st.write(
            f"- {alert['symbol']} وصل إلى ${alert['current_price']:,.2f} "
            f"والشرط كان {alert['condition']} ${alert['target_price']:,.2f}"
        )

st.markdown("## 📊 أسعار قائمة المتابعة")

if price_rows:
    prices_df = pd.DataFrame(price_rows)

    display = prices_df.copy()
    display["السعر"] = display["السعر"].apply(lambda x: f"${x:,.2f}")
    display["تغير 24h"] = display["تغير 24h"].apply(lambda x: f"{x:.2f}%")
    display["الأعلى"] = display["الأعلى"].apply(lambda x: f"${x:,.2f}")
    display["الأدنى"] = display["الأدنى"].apply(lambda x: f"${x:,.2f}")

    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("لا توجد أسعار لعرضها حالياً.")

st.divider()

st.markdown("## 🚨 إنشاء تنبيه سعري")

with st.form("alert_form"):
    alert_symbol = st.selectbox(
        "الزوج",
        SYMBOLS,
        key="alert_symbol"
    )

    condition_label = st.selectbox(
        "الشرط",
        [
            "السعر أعلى أو يساوي",
            "السعر أقل أو يساوي"
        ]
    )

    condition = ">=" if condition_label == "السعر أعلى أو يساوي" else "<="

    target_price = st.number_input(
        "السعر المستهدف",
        min_value=0.000001,
        value=100.0,
        step=1.0,
        format="%.6f"
    )

    submitted = st.form_submit_button(
        "إنشاء التنبيه",
        type="primary",
        use_container_width=True
    )

if submitted:
    ok, msg = create_alert(
        symbol=alert_symbol,
        condition=condition,
        target_price=target_price
    )

    if ok:
        st.success(msg)
        st.rerun()
    else:
        st.error(msg)

st.divider()

st.markdown("## 📜 سجل التنبيهات")

all_alerts = get_alerts(active_only=False)

if all_alerts.empty:
    st.info("لا توجد تنبيهات حالياً.")
else:
    view = all_alerts.copy()

    view["الحالة"] = view["active"].apply(lambda x: "نشط" if x == 1 else "تم التفعيل/مغلق")
    view["target_price"] = view["target_price"].apply(lambda x: f"${x:,.2f}")

    view = view.rename(
        columns={
            "id": "ID",
            "symbol": "الزوج",
            "condition": "الشرط",
            "target_price": "السعر المستهدف",
            "created_at": "تاريخ الإنشاء",
            "triggered_at": "تاريخ التفعيل",
        }
    )

    st.dataframe(
        view[
            [
                "ID",
                "الزوج",
                "الشرط",
                "السعر المستهدف",
                "الحالة",
                "تاريخ الإنشاء",
                "تاريخ التفعيل",
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

footer()
