import streamlit as st

st.set_page_config(
    page_title="Tokenomics & Roadmap | Baya Empire",
    page_icon="🧬",
    layout="wide"
)

import pandas as pd
import plotly.graph_objects as go

from src.config import TOKEN_USE_CASES, ROADMAP, LEGAL_DISCLAIMER
from src.ui import setup_style, page_header, metric_card, info_card, footer

setup_style()

page_header(
    "🧬 Tokenomics & Roadmap",
    "تصور أولي غير نهائي لاستخدامات BAYA Token وخارطة الطريق"
)

st.error(
    "تنبيه مهم: لا يوجد إطلاق رسمي لأي Token حالياً. "
    "هذه الصفحة تصور أولي تعليمي وليست عرضاً استثمارياً أو دعوة للشراء."
)

st.warning(LEGAL_DISCLAIMER)

st.markdown(
    """
    ## لماذا Token؟

    لا يجب أن تكون العملة هي البداية. البداية هي المنصة، المجتمع، الشفافية،
    والمشاريع ذات الأثر.

    إذا تم إطلاق BAYA Token مستقبلاً، يجب أن يكون له استخدام واضح داخل النظام،
    وليس مجرد أداة مضاربة.
    """
)

c1, c2, c3 = st.columns(3)

with c1:
    metric_card("الحالة", "Not Launched", "لا يوجد إطلاق رسمي", "#ff6b6b")

with c2:
    metric_card("الهدف", "Utility", "استخدام داخل المنصة", "#00f2ff")

with c3:
    metric_card("الأولوية", "Legal First", "مراجعة قانونية أولاً", "#ffaa00")

st.divider()

st.markdown("## استخدامات BAYA Token المقترحة")

for item in TOKEN_USE_CASES:
    st.write(f"- {item}")

st.divider()

st.markdown("## Tokenomics تصور أولي")

st.caption("هذه الأرقام افتراضية للنقاش فقط وليست نهائية.")

tokenomics = pd.DataFrame(
    [
        {"category": "Community Rewards", "value": 30},
        {"category": "Impact Treasury", "value": 25},
        {"category": "Ecosystem Development", "value": 20},
        {"category": "Team / Contributors", "value": 15},
        {"category": "Liquidity / Market Making", "value": 10},
    ]
)

fig = go.Figure(
    data=[
        go.Pie(
            labels=tokenomics["category"],
            values=tokenomics["value"],
            hole=0.45,
            marker=dict(
                colors=[
                    "#00f2ff",
                    "#00ff88",
                    "#ffaa00",
                    "#a855f7",
                    "#ff0055",
                ]
            )
        )
    ]
)

fig.update_layout(
    template="plotly_dark",
    height=430,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=10, r=10, t=30, b=10),
)

st.plotly_chart(fig, use_container_width=True)

st.dataframe(tokenomics, use_container_width=True, hide_index=True)

st.divider()

st.markdown("## 🗺️ Roadmap")

for phase in ROADMAP:
    st.markdown(
        f"""
        <div class="impact-card">
            <h3>{phase['phase']} — {phase['title']}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    for item in phase["items"]:
        st.write(f"- {item}")

st.divider()

st.markdown(
    """
    ## قبل أي إطلاق حقيقي للعملة

    يجب توفر هذه العناصر:

    - رأي قانوني واضح.
    - تحديد الدول المستهدفة والممنوعة.
    - Smart Contract Audit.
    - سياسة KYC/AML إذا كانت مطلوبة.
    - Whitepaper نهائي.
    - Tokenomics نهائي.
    - عدم استخدام عبارات مثل: أرباح مضمونة، 10x، استثمر الآن.
    """
)

footer()
