import streamlit as st
from src.ui import setup_style, page_header

setup_style()
page_header("مركز الدعم التقني", "نحن هنا لخدمة مواطني الإمبراطورية")

with st.form("support_form"):
    email = st.text_input("بريدك الإلكتروني")
    issue = st.selectbox("نوع المشكلة", ["مشكلة تقنية", "استفسار عن العملة", "شراكة استراتيجية"])
    message = st.text_area("رسالتك")
    submit = st.form_submit_button("إرسال الطلب")
    
    if submit:
        st.success("تم استلام رسالتك بنجاح! سيرد عليك مستشارو الإمبراطورية قريباً.")

st.markdown("---")
st.write("📱 **تابعنا على:** [Telegram] | [X/Twitter] | [Discord]")
