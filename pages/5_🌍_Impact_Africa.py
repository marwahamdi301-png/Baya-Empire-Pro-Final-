import streamlit as st
import pandas as pd

st.markdown("<h1>🌍 التأثير الإيجابي في أفريقيا</h1>", unsafe_allow_html=True)

st.success("كل صفقة تنفذها تساهم في بناء مستقبل أفضل للقارة")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("إجمالي المساهمات", "$248,750", "↑ 18% هذا الشهر")
with col2:
    st.metric("مشاريع ممولة", "47 مشروع", "↑ 9 مشاريع")
with col3:
    st.metric("مستفيدين مباشرين", "18,420 شخص", "↑ 2,340")

st.markdown("---")

st.subheader("المشاريع المدعومة حالياً")
projects = {
    "الدولة": ["كينيا", "نيجيريا", "غانا", "أوغندا", "تنزانيا"],
    "المشروع": ["بناء 12 مدرسة", "آبار مياه نظيفة", "طاقة شمسية للقرى", "تدريب رياديين شباب", "زراعة مستدامة"],
    "المبلغ المخصص": ["$68,000", "$45,200", "$52,000", "$31,500", "$29,000"],
    "الحالة": ["مكتمل 85%", "مكتمل 60%", "جاري التنفيذ", "مكتمل", "جاري التنفيذ"]
}

st.dataframe(pd.DataFrame(projects), use_container_width=True, hide_index=True)

st.markdown("### كيف تساهم؟")
st.progress(0.68)
st.caption("68% من رسوم التداول تذهب مباشرة إلى صندوق التأثير (Impact Fund)")

if st.button("انضم إلى حملة التأثير الشهرية", type="primary"):
    st.balloons()
    st.success("شكراً لك! أنت الآن جزء من بناء إمبراطورية بايا الحقيقية 🌍")
