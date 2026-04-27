import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.ui import setup_style, page_header

setup_style()
page_header("لوحة السوق العالمية", "مراقبة الأسعار والتحليل اللحظي")

# محاكاة بيانات السوق
data = {
    'العملة': ['BTC', 'ETH', 'BAYA', 'SOL'],
    'السعر ($)': [65000, 3500, 0.01, 140],
    'التغيير': ['+2.5%', '+1.8%', '+5.0%', '-0.5%']
}
df = pd.DataFrame(data)

st.table(df)

st.info("💡 نصيحة الإمبراطورية: عملة $BAYA تظهر استقراراً قوياً في مرحلة الإطلاق.")
