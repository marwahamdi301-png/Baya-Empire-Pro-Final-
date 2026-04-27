import streamlit as st
from src.ui import setup_style, page_header

setup_style()
page_header("قائمة فحص الإطلاق"، "الخطوات النهائية للسيادة الرقمية")

st.write("### ✅ المهام المكتملة")
st.checkbox("رفع ملف المكتبات (requirements.txt)"، value=True)
st.checkbox("إعداد المحرك الرئيسي (app.py)"، value=True)
st.checkbox("تصميم الهوية (src/ui.py)"، value=True)
st.checkbox("إضافة الصفحات العشر"، value=True)

st.write("### 🚀 الخطوة القادمة")
if st.button("تفعيل الرابط العالمي"):
    st.balloons()
    st.success("إمبراطورية بايا جاهزة للانطلاق! توجهي الآن إلى Streamlit Cloud لربط المستودع.")
