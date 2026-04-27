import streamlit as st
from src.ui import setup_style, page_header, metric_card, risk_notice, footer

# 1. إعداد الصفحة
st.set_page_config(page_title="Baya Empire Pro", layout="wide", page_icon="🛡️")

# 2. تفعيل التصميم الاحترافي
setup_style()

# 3. رأس الصفحة
page_header("🛡️ BAYA EMPIRE PRO", "منصة تداول ذكية ورؤية تنموية لأفريقيا")

# 4. تنبيه المخاطر
risk_notice()

# 5. القائمة التي كنتِ تحاولين إضافتها (تُكتب هكذا برمجياً)
st.markdown("## 🧭 خارطة الإمبراطورية")
st.markdown("""
- **Market**: شارتات حية مع RSI و SMA و EMA و MACD.
- **AI Signals**: إشارات تعليمية مبنية على تحليل فني ذكي.
- **Portfolio**: محفظة افتراضية لمتابعة الأداء والعمليات.
- **Africa Impact**: رؤية المشروع لدعم المبادرات الأفريقية.
- **Watchlist & Alerts**: متابعة العملات المفضلة وتنبيهات السعر.
- **Whitepaper**: الدليل التقني والرؤية الكاملة للمشروع.
- **Admin**: لوحة التحكم المركزية (محمية بكلمة مرور).
""")

# 6. تذييل الصفحة
footer()
