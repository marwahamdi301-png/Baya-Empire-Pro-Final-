import streamlit as st

st.set_page_config(
    page_title="Africa Impact | Baya Empire",
    page_icon="🌍",
    layout="wide"
)

import pandas as pd

from src.ui import setup_style, page_header, metric_card, footer

setup_style()

page_header(
    "🌍 Baya Empire Impact",
    "منصة رقمية شفافة لدعم مشاريع تنموية في دول أفريقية"
)

st.markdown(
    """
    ## لماذا Baya Empire Impact؟

    لأن الهدف ليس فقط متابعة الأسواق أو بناء محفظة افتراضية، بل بناء مجتمع رقمي
    يستطيع لاحقاً دعم مشاريع حقيقية في أفريقيا بطريقة شفافة ومنظمة.

    المجالات المستهدفة:

    - التعليم الرقمي.
    - الطاقة الشمسية.
    - المياه.
    - الزراعة.
    - ريادة الأعمال.
    - تمويل المشاريع الصغيرة.
    """
)

c1, c2, c3 = st.columns(3)

with c1:
    metric_card("🎯 الرؤية", "Impact First", "الأثر قبل المضاربة", "#00f2ff")

with c2:
    metric_card("🔍 الشفافية", "Trackable", "تتبع المشاريع والتمويل", "#ffaa00")

with c3:
    metric_card("🤝 المجتمع", "Community", "تصويت ومشاركة", "#00ff88")

st.divider()

projects = pd.DataFrame(
    [
        {
            "الدولة": "كينيا",
            "المشروع": "طاقة شمسية لمدرسة ريفية",
            "القطاع": "طاقة / تعليم",
            "الهدف": 12000,
            "المجمع": 3500,
            "الحالة": "قيد التمويل",
        },
        {
            "الدولة": "السنغال",
            "المشروع": "دعم تعاونية زراعية للشباب",
            "القطاع": "زراعة",
            "الهدف": 8000,
            "المجمع": 2100,
            "الحالة": "قيد التحقق",
        },
        {
            "الدولة": "المغرب",
            "المشروع": "تكوين رقمي للشباب",
            "القطاع": "تعليم رقمي",
            "الهدف": 5000,
            "المجمع": 1200,
            "الحالة": "قيد التمويل",
        },
        {
            "الدولة": "غانا",
            "المشروع": "معدات لمركز تدريب مهني",
            "القطاع": "تكوين / شباب",
            "الهدف": 15000,
            "المجمع": 6000,
            "الحالة": "قيد التمويل",
        },
    ]
)

st.markdown("## 📌 مشاريع تجريبية للعرض")

st.dataframe(projects, use_container_width=True, hide_index=True)

st.markdown("## 📊 تقدم المشاريع")

for _, row in projects.iterrows():
    progress = min(row["المجمع"] / row["الهدف"], 1)

    st.markdown(
        f"""
        <div class="impact-card">
            <h3>{row['المشروع']} — {row['الدولة']}</h3>
            <p>القطاع: {row['القطاع']} | الحالة: {row['الحالة']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(progress)
    st.caption(
        f"تم جمع ${row['المجمع']:,} من أصل ${row['الهدف']:,} "
        f"({progress * 100:.1f}%)"
    )

st.divider()

st.markdown(
    """
    ## تنبيه قانوني مهم

    أي Token أو عملة مستقبلية يجب أن تمر عبر مراجعة قانونية وتنظيمية.
    لا يجب تسويق المشروع على أنه يضمن أرباحاً أو عوائد مالية.
    الأفضل أن يكون التركيز على الشفافية، الأثر، والمجتمع.
    """
)

footer()
