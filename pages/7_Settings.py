import streamlit as st
from src.ui import setup_style, page_header

setup_style()
page_header("الإعدادات والأمان", "تخصيص تجربتك وحماية أصولك")

st.write("### 🔐 حماية الحساب")
st.toggle("تفعيل التحقق الثنائي (2FA)", value=True)
st.toggle("تنبيهات تسجيل الدخول عبر البريد")

st.write("### 🎨 التفضيلات")
language = st.selectbox("لغة الواجهة", ["العربية", "English", "Français"])
theme = st.select_slider("كثافة اللون السيان", options=["هادئ", "متوسط", "إمبراطوري"])

if st.button("حفظ التغييرات"):
    st.success(f"تم حفظ الإعدادات بنجاح! لغتك المختارة: {language}")
