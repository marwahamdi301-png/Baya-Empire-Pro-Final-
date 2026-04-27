import streamlit as st

st.set_page_config(
    page_title="Community | Baya Empire",
    page_icon="🤝",
    layout="wide"
)

from src.config import (
    AFRICAN_COUNTRIES,
    AMBASSADOR_ROLES,
    BRAND_TAGLINE,
    LEGAL_DISCLAIMER,
)
from src.ui import setup_style, page_header, metric_card, info_card, social_buttons, footer
from src.db import init_db, add_community_lead

setup_style()
init_db()

page_header(
    "🤝 Baya Empire Community",
    "مجتمع رقمي لدعم التقنية، التعليم، والأثر في أفريقيا"
)

st.warning(LEGAL_DISCLAIMER)

st.markdown(
    f"""
    ## {BRAND_TAGLINE}

    هدف المجتمع هو بناء شبكة من المهتمين بالتقنية، Web3، التعليم، وريادة الأعمال
    لدعم مشاريع أفريقية بطريقة شفافة ومنظمة.

    نحن نبحث عن:
    - سفراء محليين.
    - صناع محتوى.
    - مطورين.
    - شركاء ميدانيين.
    - مستشارين.
    - متطوعين.
    """
)

c1, c2, c3 = st.columns(3)

with c1:
    metric_card("🌍 الرؤية", "Africa Impact", "مجتمع يخدم الأثر", "#00f2ff")

with c2:
    metric_card("🤝 النمو", "Ambassadors", "سفراء في دول أفريقية", "#ffaa00")

with c3:
    metric_card("🔍 الثقة", "Transparency", "شفافية ومتابعة", "#00ff88")

st.divider()

st.markdown("## 🧭 مبادئ المجتمع")

col1, col2 = st.columns(2)

with col1:
    info_card(
        "الأثر أولاً",
        "لا نبيع وعوداً فارغة. نركز على مشاريع قابلة للتتبع ونتائج واضحة.",
        "🎯"
    )

    info_card(
        "الشفافية",
        "كل مشروع يجب أن يعرض هدفه، تقدمه، حالته، وتقاريره كلما أمكن.",
        "🔍"
    )

with col2:
    info_card(
        "التعليم",
        "نستخدم السوق والمحفظة الافتراضية والإشارات كأدوات تعليمية لا كوعود ربح.",
        "📚"
    )

    info_card(
        "المشاركة",
        "المجتمع يشارك في التصويت، الاقتراح، النشر، والتحقق من المشاريع.",
        "🗳️"
    )

st.divider()

st.markdown("## 🚀 انضم كمشارك أو سفير")

with st.form("community_form"):
    name = st.text_input("الاسم الكامل")
    country = st.selectbox("الدولة", AFRICAN_COUNTRIES)
    role = st.selectbox("الدور الذي تريد المشاركة به", AMBASSADOR_ROLES)
    contact = st.text_input("وسيلة التواصل: Email / Telegram / WhatsApp")
    message = st.text_area("رسالة قصيرة عن سبب اهتمامك بالمشروع")

    submitted = st.form_submit_button(
        "إرسال طلب الانضمام",
        type="primary",
        use_container_width=True
    )

if submitted:
    if not name.strip():
        st.error("الاسم مطلوب.")
    elif not contact.strip():
        st.error("وسيلة التواصل مطلوبة.")
    else:
        add_community_lead(
            name=name.strip(),
            country=country,
            role=role,
            contact=contact.strip(),
            message=message.strip()
        )
        st.success("تم إرسال طلبك بنجاح. مرحباً بك في مجتمع Baya Empire.")

st.divider()

social_buttons()

footer()
