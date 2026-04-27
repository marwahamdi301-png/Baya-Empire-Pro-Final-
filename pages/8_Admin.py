import streamlit as st

st.set_page_config(
    page_title="Admin | Baya Empire",
    page_icon="🛠️",
    layout="wide"
)

import pandas as pd

from src.ui import setup_style, page_header, metric_card, footer
from src.auth import require_admin, logout_admin
from src.db import (
    init_db,
    get_projects,
    add_project,
    update_project,
    delete_project
)

setup_style()
init_db()
require_admin()

page_header(
    "🛠️ Admin Dashboard",
    "إدارة مشاريع Africa Impact"
)

logout_admin()

st.warning(
    "هذه الصفحة مخصصة للإدارة. لا تضف مشاريع حقيقية قبل التحقق من البيانات والشركاء المحليين."
)

st.divider()

tab_add, tab_manage = st.tabs(
    [
        "➕ إضافة مشروع",
        "📌 إدارة المشاريع"
    ]
)

with tab_add:
    st.markdown("## ➕ إضافة مشروع جديد")

    with st.form("add_project_form"):
        country = st.text_input("الدولة", value="كينيا")
        name = st.text_input("اسم المشروع")
        sector = st.text_input("القطاع", value="تعليم / طاقة")
        target = st.number_input("الهدف المالي", min_value=1.0, value=10000.0, step=500.0)
        raised = st.number_input("المبلغ المجمع", min_value=0.0, value=0.0, step=100.0)

        status = st.selectbox(
            "الحالة",
            [
                "قيد التحقق",
                "قيد التمويل",
                "ممول جزئياً",
                "مكتمل",
                "متوقف"
            ]
        )

        description = st.text_area("وصف المشروع")

        submitted = st.form_submit_button(
            "إضافة المشروع",
            type="primary",
            use_container_width=True
        )

    if submitted:
        if not name.strip():
            st.error("اسم المشروع مطلوب.")
        elif not description.strip():
            st.error("وصف المشروع مطلوب.")
        else:
            add_project(
                country=country,
                name=name,
                sector=sector,
                target=target,
                raised=raised,
                status=status,
                description=description
            )

            st.success("تمت إضافة المشروع بنجاح.")
            st.rerun()

with tab_manage:
    st.markdown("## 📌 إدارة المشاريع")

    projects = get_projects()

    if projects.empty:
        st.info("لا توجد مشاريع.")
        st.stop()

    display = projects.copy()

    display["target"] = display["target"].apply(lambda x: f"${x:,.0f}")
    display["raised"] = display["raised"].apply(lambda x: f"${x:,.0f}")

    display = display.rename(
        columns={
            "id": "ID",
            "country": "الدولة",
            "name": "المشروع",
            "sector": "القطاع",
            "target": "الهدف",
            "raised": "المجمع",
            "status": "الحالة",
            "votes": "الأصوات",
            "created_at": "تاريخ الإضافة",
        }
    )

    st.dataframe(
        display[
            [
                "ID",
                "الدولة",
                "المشروع",
                "القطاع",
                "الهدف",
                "المجمع",
                "الحالة",
                "الأصوات",
                "تاريخ الإضافة",
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.markdown("## تحديث مشروع")

    project_options = {
        f"{row['id']} — {row['name']}": int(row["id"])
        for _, row in projects.iterrows()
    }

    selected_label = st.selectbox(
        "اختر المشروع",
        list(project_options.keys())
    )

    selected_id = project_options[selected_label]
    selected_row = projects[projects["id"] == selected_id].iloc[0]

    with st.form("update_project_form"):
        new_raised = st.number_input(
            "المبلغ المجمع الجديد",
            min_value=0.0,
            value=float(selected_row["raised"]),
            step=100.0
        )

        new_status = st.selectbox(
            "الحالة الجديدة",
            [
                "قيد التحقق",
                "قيد التمويل",
                "ممول جزئياً",
                "مكتمل",
                "متوقف"
            ],
            index=[
                "قيد التحقق",
                "قيد التمويل",
                "ممول جزئياً",
                "مكتمل",
                "متوقف"
            ].index(selected_row["status"]) if selected_row["status"] in [
                "قيد التحقق",
                "قيد التمويل",
                "ممول جزئياً",
                "مكتمل",
                "متوقف"
            ] else 0
        )

        update_submitted = st.form_submit_button(
            "تحديث المشروع",
            type="primary",
            use_container_width=True
        )

    if update_submitted:
        update_project(
            project_id=selected_id,
            raised=new_raised,
            status=new_status
        )

        st.success("تم تحديث المشروع.")
        st.rerun()

    st.divider()

    with st.expander("⚠️ حذف مشروع"):
        st.warning("الحذف نهائي وسيحذف أيضاً أصوات المشروع.")

        confirm_delete = st.checkbox(
            f"أؤكد حذف المشروع: {selected_row['name']}"
        )

        if st.button("حذف المشروع", type="secondary"):
            if confirm_delete:
                delete_project(selected_id)
                st.success("تم حذف المشروع.")
                st.rerun()
            else:
                st.warning("يجب تأكيد الحذف أولاً.")

footer()
