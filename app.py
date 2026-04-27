import streamlit as st
from src.ui import setup_style, page_header, footer
from src.config import APP_NAME

# إعداد الصفحة
st.set_page_config(page_title=APP_NAME, layout="wide", initial_sidebar_state="expanded")
setup_style()

# المحتوى الرئيسي
page_header("إمبراطورية بايا البرمجية", "منصة التداول الذكية والأثر الأفريقي المستدام")

st.markdown(f"""
### 🛡️ مرحباً بك في النسخة المتطورة
لقد تم تفعيل المحرك الرئيسي بنجاح. يمكنك الآن التنقل بين صفحات الإمبراطورية عبر القائمة الجانبية:
1. **السوق المباشر:** لمتابعة الأسعار لحظياً.
2. **الذكاء الاصطناعي:** لتحليل الإشارات الفنية.
3. **اقتصاد $BAYA:** للتحكم في إصدار العملة الحقيقي.
""")

col1, col2 = st.columns(2)
with col1:
    st.info("💎 **حالة العملة:** جاهزة للإطلاق")
with col2:
    st.success("🌍 **الأثر:** متصل بشبكة المشاريع الأفريقية")

footer()
