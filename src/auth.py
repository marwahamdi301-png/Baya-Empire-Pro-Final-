src/auth.py
import streamlit as st


def get_admin_password():
    try:
        return st.secrets.get("ADMIN_PASSWORD", None)
    except Exception:
        return None


def require_admin():
    if "is_admin" not in st.session_state:
        st.session_state.is_admin = False

    if st.session_state.is_admin:
        return True

    st.warning("هذه الصفحة مخصصة للإدارة فقط.")

    admin_password = get_admin_password()

    if not admin_password:
        st.error(
            "لم يتم ضبط كلمة مرور الإدارة. "
            "أضف ADMIN_PASSWORD داخل Streamlit Secrets."
        )
        st.stop()

    password = st.text_input(
        "كلمة مرور الإدارة",
        type="password"
    )

    if st.button("دخول"):
        if password == admin_password:
            st.session_state.is_admin = True
            st.success("تم تسجيل الدخول.")
            st.rerun()
        else:
            st.error("كلمة المرور غير صحيحة.")

    st.stop()


def logout_admin():
    if st.button("تسجيل خروج الإدارة"):
        st.session_state.is_admin = False
        st.rerun()
