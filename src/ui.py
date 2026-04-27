def info_card(title, text, icon=""):
    st.markdown(
        f"""
        <div class="impact-card">
            <h3>{icon} {title}</h3>
            <p>{text}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def social_buttons():
    from src.config import SOCIAL_LINKS

    st.markdown("### روابط المجتمع الرسمية")

    cols = st.columns(len(SOCIAL_LINKS))

    for col, (name, link) in zip(cols, SOCIAL_LINKS.items()):
        with col:
            st.link_button(
                name,
                link,
                use_container_width=True
            )


def launch_badge(label, status="قيد التطوير"):
    color = "#ffaa00"

    if status == "جاهز":
        color = "#00ff88"
    elif status == "غير جاهز":
        color = "#ff0055"

    st.markdown(
        f"""
        <div style="
            background: rgba(255,255,255,0.045);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 16px;
            padding: 14px;
            margin-bottom: 8px;
        ">
            <b>{label}</b>
            <span style="float:left; color:{color}; font-weight:900;">
                {status}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )
