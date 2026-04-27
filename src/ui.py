import streamlit as st

def setup_style():
    st.markdown("""
        <style>
        .stApp {
            background-color: #0e1117;
            color: #ffffff;
        }
        .main-header {
            color: #00f2ff;
            text-align: center;
            font-size: 2.5rem;
            font-weight: bold;
            text-shadow: 0 0 10px #00f2ff;
        }
        .stButton>button {
            background-color: #00f2ff;
            color: black;
            border-radius: 10px;
            border: none;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

def page_header(title, subtitle):
    st.markdown(f'<p class="main-header">{title}</p>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align:center; color:#888;">{subtitle}</p>', unsafe_allow_html=True)
    st.divider()

def footer():
    st.divider()
    st.markdown('<p style="text-align:center; color:#555;">© 2026 Baya Empire Pro - All Rights Reserved</p>', unsafe_allow_html=True)
