import streamlit as st

st.set_page_config(
    page_title="Portfolio | Baya Empire",
    page_icon="💼",
    layout="wide"
)

import pandas as pd

from src.config import DATA_SOURCES, SYMBOLS, PAPER_FEE_RATE, INITIAL_CASH
from src.ui import setup_style, page_header, metric_card, risk_notice, footer
from src.data import get_ticker
from src.db import (
    init_db,
    get_cash,
    get_positions,
    get_trades,
    execute_trade,
    reset_portfolio
)

setup_style()
init_db()

with st.sidebar:
    st.markdown("## 💼 Portfolio Settings")

    data_source = st.selectbox(
        "مصدر البيانات",
        list(DATA_SOURCES.keys()),
        index=0
    )

    base_url = DATA_SOURCES[data_source]

    symbol = st.selectbox(
        "زوج العملية",
        SYMBOLS,
        index=0
    )

page_header(
    "💼 Virtual Portfolio",
    "محفظة افتراضية للتجربة والتعلم بدون تداول حقيقي"
)

risk_notice()

ticker, error = get_ticker(symbol, base_url)

if not ticker:
    st.error(f"تعذر جلب سعر {symbol}: {error}")
    st.stop()

cash = get_cash()
positions = get_positions()

price_map = {}
for sym in SYMBOLS:
    t, _ = get_ticker(sym, base_url)
    if t:
        price_map[sym] = t["price"]

portfolio_value = cash
unrealized_pnl = 0.0
invested_value = 0.0

if not positions.empty:
    positions_calc = positions.copy()
    positions_calc["current_price"] = positions_calc["symbol"].map(price_map)
    positions_calc = positions_calc.dropna(subset=["current_price"])

    positions_calc["market_value"] = positions_calc["qty"] * positions_calc["current_price"]
    positions_calc["cost_value"] = positions_calc["qty"] * positions_calc["avg_price"]
    positions_calc["unrealized_pnl"] = positions_calc["market_value"] - positions_calc["cost_value"]
    positions_calc["unrealized_pnl_pct"] = (
        positions_calc["unrealized_pnl"] / positions_calc["cost_value"]
    ) * 100

    invested_value = positions_calc["market_value"].sum()
    unrealized_pnl = positions_calc["unrealized_pnl"].sum()
    portfolio_value = cash + invested_value
else:
    positions_calc = pd.DataFrame()

total_pnl = portfolio_value - INITIAL_CASH
total_pnl_pct = (total_pnl / INITIAL_CASH) * 100
pnl_color = "#00ff88" if total_pnl >= 0 else "#ff0055"

c1, c2, c3, c4 = st.columns(4)

with c1:
    metric_card("الرصيد النقدي", f"${cash:,.2f}", "Paper Cash", "#00f2ff")

with c2:
    metric_card("قيمة المراكز", f"${invested_value:,.2f}", "Market Value", "#ffaa00")

with c3:
    metric_card("قيمة المحفظة", f"${portfolio_value:,.2f}", "Cash + Positions", "#ffffff")

with c4:
    metric_card("PnL الإجمالي", f"${total_pnl:,.2f} / {total_pnl_pct:.2f}%", "من البداية", pnl_color)

st.divider()

tab_trade, tab_positions, tab_history = st.tabs(
    ["⚡ تنفيذ ورقي", "📌 المراكز", "📜 السجل"]
)

with tab_trade:
    st.markdown("### ⚡ تنفيذ عملية افتراضية")

    st.info(
        f"السعر الحالي لـ {symbol}: ${ticker['price']:,.2f} | "
        f"رسوم افتراضية: {PAPER_FEE_RATE * 100:.2f}%"
    )

    with st.form("paper_trade_form"):
        side = st.radio(
            "نوع العملية",
            ["BUY", "SELL"],
            horizontal=True
        )

        amount = st.number_input(
            "الكمية",
            min_value=0.000001,
            value=0.1,
            step=0.01,
            format="%.6f"
        )

        estimated_total = amount * ticker["price"]
        estimated_fee = estimated_total * PAPER_FEE_RATE

        st.write(f"القيمة التقريبية: **${estimated_total:,.2f}**")
        st.write(f"الرسوم التقريبية: **${estimated_fee:,.2f}**")

        confirm = st.checkbox(
            "أفهم أن هذه عملية ورقية وليست تداولاً حقيقياً."
        )

        submitted = st.form_submit_button(
            "تنفيذ العملية الورقية",
            type="primary",
            use_container_width=True
        )

    if submitted:
        if not confirm:
            st.warning("يجب تأكيد أن العملية تجريبية.")
        else:
            ok, msg = execute_trade(
                symbol=symbol,
                side=side,
                price=ticker["price"],
                amount=amount
            )

            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

with tab_positions:
    st.markdown("### 📌 المراكز المفتوحة")

    if positions_calc.empty:
        st.info("لا توجد مراكز مفتوحة حالياً.")
    else:
        view = positions_calc.copy()

        view = view.rename(
            columns={
                "symbol": "الزوج",
                "qty": "الكمية",
                "avg_price": "متوسط الدخول",
                "current_price": "السعر الحالي",
                "market_value": "القيمة السوقية",
                "unrealized_pnl": "PnL غير محقق",
                "unrealized_pnl_pct": "PnL %",
                "realized_pnl": "PnL محقق",
            }
        )

        for col in ["متوسط الدخول", "السعر الحالي", "القيمة السوقية", "PnL غير محقق", "PnL محقق"]:
            view[col] = view[col].apply(lambda x: f"${x:,.2f}")

        view["الكمية"] = view["الكمية"].apply(lambda x: f"{x:,.6f}")
        view["PnL %"] = view["PnL %"].apply(lambda x: f"{x:.2f}%")

        st.dataframe(
            view[
                [
                    "الزوج",
                    "الكمية",
                    "متوسط الدخول",
                    "السعر الحالي",
                    "القيمة السوقية",
                    "PnL غير محقق",
                    "PnL %",
                    "PnL محقق",
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

with tab_history:
    st.markdown("### 📜 سجل العمليات")

    trades = get_trades(limit=100)

    if trades.empty:
        st.info("لا توجد عمليات حتى الآن.")
    else:
        display = trades.copy()

        for col in ["السعر", "الإجمالي", "الرسوم"]:
            display[col] = display[col].apply(lambda x: f"${x:,.2f}")

        display["الكمية"] = display["الكمية"].apply(lambda x: f"{x:,.6f}")

        st.dataframe(
            display,
            use_container_width=True,
            hide_index=True
        )

        csv = trades.to_csv(index=False).encode("utf-8-sig")

        st.download_button(
            "تحميل السجل CSV",
            data=csv,
            file_name="baya_portfolio_trades.csv",
            mime="text/csv",
            use_container_width=True
        )

st.divider()

with st.expander("⚠️ إعادة ضبط المحفظة"):
    st.warning("هذا سيمسح كل العمليات والمراكز ويعيد الرصيد الافتراضي من البداية.")

    if st.button("إعادة ضبط المحفظة", type="secondary"):
        reset_portfolio()
        st.success("تمت إعادة ضبط المحفظة.")
        st.rerun()

footer()
