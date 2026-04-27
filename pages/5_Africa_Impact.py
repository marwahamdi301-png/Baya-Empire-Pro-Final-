import uuid

import streamlit as st

st.set_page_config(
    page_title="Africa Impact | Baya Empire",
    page_icon="🌍",
    layout="wide"
)

import pandas as pd

from src.ui import setup_style, page_header, metric_card, footer
from src.db import init_db, get_projects, vote_project

setup_style()
init_db()

if "voter_key" not in st.session_state:
    st.session_state.voter_key = str(uuid.uuid4())

page_header(
    "🌍 Baya Empire Impact",
    "منصة رقمية شفافة لدعم مشاريع تنموية في دول أفريقية"
)

st.markdown(
    """
    ## لماذا Baya Empire Impact؟

    لأن الهدف ليس مجرد متابعة الأسواق، بل بناء مجتمع رقمي يستطيع دعم مشاريع
    تنموية حقيقية في أفريقيا بطريقة شفافة ومنظمة.

    المنصة تستهدف قطاعات مثل:

    - التعليم الرقمي.
    - الطاقة الشمسية.
    - المياه.
    - الزراعة.
    - ريادة الأعمال.
    - المشاريع الصغيرة.
    """
)

c1, c2, c3 = st.columns(3)

with c1:
    metric_card("🎯 الرؤية", "Impact First", "الأثر قبل المضاربة", "#00f2ff")

with c2:
    metric_card("🔍 الشفافية", "Trackable", "تتبع التمويل والتقدم", "#ffaa00")

with c3:
    metric_card("🤝 المجتمع", "Voting", "تصويت ومشاركة", "#00ff88")

st.divider()

projects = get_projects()

if projects.empty:
    st.info("لا توجد مشاريع حالياً.")
    st.stop()

total_target = projects["target"].sum()
total_raised = projects["raised"].sum()
total_votes = projects["votes"].sum()

m1, m2, m3 = st.columns(3)

with m1:
    metric_card("إجمالي الأهداف", f"${total_target:,.0f}", "لكل المشاريع", "#00f2ff")

with m2:
    metric_card("إجمالي المجمع", f"${total_raised:,.0f}", "تمويل تجريبي", "#00ff88")

with m3:
    metric_card("عدد الأصوات", f"{int(total_votes)}", "تصويت مجتمعي", "#ffaa00")

st.divider()

st.markdown("## 📌 المشاريع")

for _, row in projects.iterrows():
    progress = 0

    if row["target"] > 0:
        progress = min(row["raised"] / row["target"], 1)

    st.markdown(
        f"""
        <div class="impact-card">
            <h3>{row['name']} — {row['country']}</h3>
            <p><b>القطاع:</b> {row['sector']} | <b>الحالة:</b> {row['status']}</p>
            <p>{row['description']}</p>
            <p><b>الأصوات:</b> {int(row['votes'])}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(progress)

    st.caption(
        f"تم جمع ${row['raised']:,.0f} من أصل ${row['target']:,.0f} "
        f"({progress * 100:.1f}%)"
    )

    col_vote, col_info = st.columns([1, 3])

    with col_vote:
        if st.button("صوّت لهذا المشروع", key=f"vote_{row['id']}"):
            ok, msg = vote_project(
                project_id=int(row["id"]),
                voter_key=st.session_state.voter_key
            )

            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.warning(msg)

    with col_info:
        st.write("")

    st.divider()

st.markdown(
    """
    ## تنبيه مهم

    المشاريع المعروضة حالياً تجريبية/نموذجية. عند إطلاق منصة حقيقية، يجب التحقق من كل مشروع،
    ونشر بيانات واضحة، وتقارير، وشركاء محليين، ومحافظ شفافة إن تم استخدام أصول رقمية.
    """
)

footer()
