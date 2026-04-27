تمام. نكمل الآن **مرحلة ما قبل الرفع**: نضيف صفحات تجعل المنصة تبدو كمشروع حقيقي قابل للنشر، ثم نعطيك خطوات الرفع على GitHub وStreamlit Cloud.

سنضيف الآن:

1. **صفحة Community / السفراء**
2. **صفحة Tokenomics & Roadmap**
3. **صفحة Launch Checklist**
4. **نموذج انضمام للمجتمع**
5. **تحديثات بسيطة في قاعدة البيانات**
6. **ملفات الرفع النهائية: `.gitignore`, `README.md`, `.streamlit/config.toml`**
7. **خطة رفع التطبيق**

> ملاحظة: سنرفع أول نسخة كـ **MVP تجريبي**. لا تطلق العملة أو تجمع أموالاً قبل المراجعة القانونية.

---

# 1) تحديث `src/config.py`

افتح:

```text
src/config.py
```

وأضف في آخر الملف:

```python
APP_VERSION = "MVP 0.3"

BRAND_TAGLINE = "Technology for African Impact"

LEGAL_DISCLAIMER = (
    "Baya Empire منصة تعليمية وتجريبية قيد التطوير. "
    "المعلومات والإشارات ليست نصيحة مالية أو استثمارية أو قانونية. "
    "لا توجد أرباح مضمونة، وأي Token مستقبلي يجب أن يخضع لمراجعة قانونية وتنظيمية."
)

SOCIAL_LINKS = {
    "Telegram": "https://t.me/your_channel",
    "X / Twitter": "https://x.com/your_account",
    "Discord": "https://discord.gg/your_server",
    "LinkedIn": "https://linkedin.com/company/your_company",
}

AMBASSADOR_ROLES = [
    "سفير دولة",
    "صانع محتوى",
    "مطوّر",
    "محلل بيانات",
    "شريك محلي",
    "مستشار قانوني",
    "مستثمر أثر",
    "متطوع",
]

AFRICAN_COUNTRIES = [
    "المغرب",
    "الجزائر",
    "تونس",
    "مصر",
    "السنغال",
    "كينيا",
    "نيجيريا",
    "غانا",
    "رواندا",
    "إثيوبيا",
    "ساحل العاج",
    "جنوب أفريقيا",
    "تنزانيا",
    "أوغندا",
    "مالي",
    "موريتانيا",
    "دولة أخرى",
]

TOKEN_USE_CASES = [
    "تصويت مجتمعي على المشاريع",
    "وصول إلى تقارير Impact",
    "مكافآت مشاركة غير مضمونة",
    "حوكمة مستقبلية بعد الإطار القانوني",
    "دعم خزينة مشاريع تنموية بشفافية",
]

ROADMAP = [
    {
        "phase": "Phase 1",
        "title": "MVP Launch",
        "items": [
            "Market Dashboard",
            "AI Signals تعليمية",
            "Portfolio افتراضي",
            "Africa Impact",
            "Watchlist & Alerts",
            "Whitepaper أولي",
        ],
    },
    {
        "phase": "Phase 2",
        "title": "Community Growth",
        "items": [
            "إطلاق Telegram / Discord",
            "فتح باب السفراء",
            "حملات محتوى يومية",
            "جمع مشاريع أفريقية مقترحة",
        ],
    },
    {
        "phase": "Phase 3",
        "title": "Transparency Layer",
        "items": [
            "تقارير شهرية",
            "لوحة مشاريع موثقة",
            "تصويت مجتمعي",
            "شركاء محليون للتحقق",
        ],
    },
    {
        "phase": "Phase 4",
        "title": "Professional Infrastructure",
        "items": [
            "نقل قاعدة البيانات إلى Supabase/PostgreSQL",
            "تسجيل دخول للمستخدمين",
            "صلاحيات Admin",
            "لوحة إحصائيات متقدمة",
        ],
    },
    {
        "phase": "Phase 5",
        "title": "Token Readiness",
        "items": [
            "مراجعة قانونية",
            "تصميم Tokenomics نهائي",
            "Smart Contract Audit",
            "Testnet",
            "إطلاق تدريجي إذا كان قانونياً وآمناً",
        ],
    },
]
```

غيّر روابط Telegram وX وDiscord لاحقاً عندما تفتح الحسابات الرسمية.

---

# 2) تحديث `src/db.py`

نضيف جدول طلبات الانضمام للمجتمع والسفراء.

داخل دالة `init_db()` في ملف:

```text
src/db.py
```

أضف هذا الجزء بعد جداول `alerts`:

```python
        # Community Leads / Ambassadors
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS community_leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                country TEXT NOT NULL,
                role TEXT NOT NULL,
                contact TEXT NOT NULL,
                message TEXT,
                created_at TEXT NOT NULL
            )
            """
        )
```

ثم أضف هذه الدوال في آخر ملف `src/db.py`:

```python
# =========================
# Community Leads
# =========================

def add_community_lead(name, country, role, contact, message):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO community_leads
            (name, country, role, contact, message, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                country,
                role,
                contact,
                message,
                now
            )
        )


def get_community_leads(limit=200):
    with get_conn() as conn:
        return pd.read_sql_query(
            """
            SELECT
                id,
                name,
                country,
                role,
                contact,
                message,
                created_at
            FROM community_leads
            ORDER BY id DESC
            LIMIT ?
            """,
            conn,
            params=(limit,)
        )
```

---

# 3) تحديث `src/ui.py`

افتح:

```text
src/ui.py
```

وأضف هذه الدوال في آخر الملف:

```python
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
```

---

# 4) إضافة صفحة Community

أنشئ ملف جديد:

```text
pages/8_Community.py
```

وضع داخله:

```python
import streamlit as st

st.set_page_config(
    page_title="Community | Baya Empire",
    page_icon="🤝",
    layout="wide"
)

from src.config import (
    AFRICAN_COUNTRIES,
    AMBASSADOR_ROLES,
    BRAND_TAGLINE,
    LEGAL_DISCLAIMER,
)
from src.ui import setup_style, page_header, metric_card, info_card, social_buttons, footer
from src.db import init_db, add_community_lead

setup_style()
init_db()

page_header(
    "🤝 Baya Empire Community",
    "مجتمع رقمي لدعم التقنية، التعليم، والأثر في أفريقيا"
)

st.warning(LEGAL_DISCLAIMER)

st.markdown(
    f"""
    ## {BRAND_TAGLINE}

    هدف المجتمع هو بناء شبكة من المهتمين بالتقنية، Web3، التعليم، وريادة الأعمال
    لدعم مشاريع أفريقية بطريقة شفافة ومنظمة.

    نحن نبحث عن:
    - سفراء محليين.
    - صناع محتوى.
    - مطورين.
    - شركاء ميدانيين.
    - مستشارين.
    - متطوعين.
    """
)

c1, c2, c3 = st.columns(3)

with c1:
    metric_card("🌍 الرؤية", "Africa Impact", "مجتمع يخدم الأثر", "#00f2ff")

with c2:
    metric_card("🤝 النمو", "Ambassadors", "سفراء في دول أفريقية", "#ffaa00")

with c3:
    metric_card("🔍 الثقة", "Transparency", "شفافية ومتابعة", "#00ff88")

st.divider()

st.markdown("## 🧭 مبادئ المجتمع")

col1, col2 = st.columns(2)

with col1:
    info_card(
        "الأثر أولاً",
        "لا نبيع وعوداً فارغة. نركز على مشاريع قابلة للتتبع ونتائج واضحة.",
        "🎯"
    )

    info_card(
        "الشفافية",
        "كل مشروع يجب أن يعرض هدفه، تقدمه، حالته، وتقاريره كلما أمكن.",
        "🔍"
    )

with col2:
    info_card(
        "التعليم",
        "نستخدم السوق والمحفظة الافتراضية والإشارات كأدوات تعليمية لا كوعود ربح.",
        "📚"
    )

    info_card(
        "المشاركة",
        "المجتمع يشارك في التصويت، الاقتراح، النشر، والتحقق من المشاريع.",
        "🗳️"
    )

st.divider()

st.markdown("## 🚀 انضم كمشارك أو سفير")

with st.form("community_form"):
    name = st.text_input("الاسم الكامل")
    country = st.selectbox("الدولة", AFRICAN_COUNTRIES)
    role = st.selectbox("الدور الذي تريد المشاركة به", AMBASSADOR_ROLES)
    contact = st.text_input("وسيلة التواصل: Email / Telegram / WhatsApp")
    message = st.text_area("رسالة قصيرة عن سبب اهتمامك بالمشروع")

    submitted = st.form_submit_button(
        "إرسال طلب الانضمام",
        type="primary",
        use_container_width=True
    )

if submitted:
    if not name.strip():
        st.error("الاسم مطلوب.")
    elif not contact.strip():
        st.error("وسيلة التواصل مطلوبة.")
    else:
        add_community_lead(
            name=name.strip(),
            country=country,
            role=role,
            contact=contact.strip(),
            message=message.strip()
        )
        st.success("تم إرسال طلبك بنجاح. مرحباً بك في مجتمع Baya Empire.")

st.divider()

social_buttons()

footer()
```

---

# 5) إضافة صفحة Tokenomics & Roadmap

أنشئ ملف جديد:

```text
pages/9_Tokenomics_Roadmap.py
```

وضع داخله:

```python
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
```

---

# 6) إضافة صفحة Launch Checklist

أنشئ ملف جديد:

```text
pages/10_Launch_Checklist.py
```

وضع داخله:

```python
import streamlit as st

st.set_page_config(
    page_title="Launch Checklist | Baya Empire",
    page_icon="✅",
    layout="wide"
)

from src.ui import setup_style, page_header, metric_card, launch_badge, footer
from src.config import LEGAL_DISCLAIMER

setup_style()

page_header(
    "✅ Launch Checklist",
    "قائمة فحص قبل نشر منصة Baya Empire للناس"
)

st.warning(LEGAL_DISCLAIMER)

st.markdown(
    """
    هذه الصفحة تساعدك على معرفة هل المنصة جاهزة للنشر الأولي أم لا.
    الهدف الآن هو نشر **MVP تجريبي** وليس إطلاق Token أو جمع أموال.
    """
)

st.divider()

checks = {
    "الكود يعمل محلياً بدون أخطاء": st.checkbox("الكود يعمل محلياً بدون أخطاء"),
    "requirements.txt موجود": st.checkbox("requirements.txt موجود"),
    "لا توجد API Keys داخل الكود": st.checkbox("لا توجد API Keys داخل الكود"),
    "ADMIN_PASSWORD موجود في Streamlit Secrets": st.checkbox("ADMIN_PASSWORD موجود في Streamlit Secrets"),
    "صفحة Africa Impact واضحة": st.checkbox("صفحة Africa Impact واضحة"),
    "صفحة Whitepaper موجودة": st.checkbox("صفحة Whitepaper موجودة"),
    "تنبيه قانوني موجود": st.checkbox("تنبيه قانوني موجود"),
    "لا توجد وعود أرباح": st.checkbox("لا توجد وعود أرباح"),
    "GitHub Repo جاهز": st.checkbox("GitHub Repo جاهز"),
    "Streamlit App Public أو قابل للمشاركة": st.checkbox("Streamlit App Public أو قابل للمشاركة"),
}

done = sum(1 for v in checks.values() if v)
total = len(checks)
progress = done / total

st.progress(progress)

c1, c2, c3 = st.columns(3)

with c1:
    metric_card("المكتمل", f"{done}/{total}", "عدد البنود الجاهزة", "#00f2ff")

with c2:
    metric_card("نسبة الجاهزية", f"{progress * 100:.0f}%", "Launch Readiness", "#ffaa00")

with c3:
    status = "جاهز" if progress >= 0.85 else "قيد التطوير"
    color = "#00ff88" if progress >= 0.85 else "#ffaa00"
    metric_card("الحالة", status, "للنشر الأولي", color)

st.divider()

st.markdown("## تقييم سريع")

if progress >= 0.85:
    st.success("المنصة جاهزة تقريباً للنشر الأولي MVP.")
elif progress >= 0.60:
    st.warning("المنصة قريبة من الجاهزية، لكن تحتاج بعض التعديلات قبل النشر.")
else:
    st.error("لا أنصح بالنشر الآن. أكمل البنود الأساسية أولاً.")

st.divider()

st.markdown("## حالة المكونات")

for label, checked in checks.items():
    launch_badge(label, "جاهز" if checked else "غير جاهز")

footer()
```

---

# 7) تحديث الصفحة الرئيسية `app.py`

في `app.py` حدّث قائمة الصفحات المتوفرة إلى:

```python
st.markdown(
    """
    - **Market**: شارتات حية مع RSI و SMA و EMA و MACD.
    - **AI Signals**: إشارات تعليمية مبنية على تحليل فني.
    - **Portfolio**: محفظة افتراضية، رصيد، مراكز، PnL، وسجل عمليات.
    - **Africa Impact**: مشاريع أفريقية، تصويت، وتتبع تقدم.
    - **Watchlist & Alerts**: قائمة متابعة وتنبيهات سعرية.
    - **Whitepaper**: وثيقة تعريفية للمشروع والرؤية.
    - **Community**: صفحة المجتمع والسفراء.
    - **Tokenomics & Roadmap**: تصور أولي وخارطة الطريق.
    - **Launch Checklist**: فحص الجاهزية قبل النشر.
    - **Admin**: إدارة المشاريع، محمية بكلمة مرور.
    """
)
```

---

# 8) ملف `.streamlit/config.toml`

أنشئ مجلد:

```text
.streamlit
```

ثم داخله ملف:

```text
config.toml
```

وضع فيه:

```toml
[theme]
base = "dark"
primaryColor = "#00f2ff"
backgroundColor = "#070b14"
secondaryBackgroundColor = "#0b0f19"
textColor = "#ffffff"
font = "sans serif"

[server]
headless = true
```

---

# 9) ملف `.gitignore`

أنشئ ملف:

```text
.gitignore
```

وضع فيه:

```gitignore
# Python
__pycache__/
*.py[cod]
.venv/
venv/
env/

# Streamlit secrets
.streamlit/secrets.toml

# Local database
*.db
*.sqlite
*.sqlite3

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/

# Logs
*.log
```

مهم جداً: لا ترفع ملف `secrets.toml` إلى GitHub.

---

# 10) ملف `README.md`

أنشئ ملف:

```text
README.md
```

وضع فيه:

```markdown
# Baya Empire Pro

Baya Empire Pro is an experimental Streamlit platform combining:

- Live crypto market dashboard
- Technical indicators: RSI, SMA, EMA, MACD
- Educational AI Signals
- Virtual Portfolio / Paper Trading
- Watchlist and Price Alerts
- Africa Impact projects
- Community and ambassadors page
- Whitepaper and roadmap
- Admin dashboard

## Disclaimer

This platform is for educational and experimental purposes only.  
It does not provide financial, investment, or legal advice.  
No profits are guaranteed.  
Any future token or digital asset must go through proper legal and regulatory review.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Admin Password

Set the following secret in Streamlit Cloud:

```toml
ADMIN_PASSWORD = "your_strong_password"
```

## Project Structure

```text
app.py
requirements.txt
src/
pages/
.streamlit/
README.md
```
```

---

# 11) ملف `requirements.txt`

ابقِ الملف هكذا:

```txt
streamlit
pandas
requests
plotly
streamlit-autorefresh
```

وجود `requirements.txt` مهم عند النشر؛ لأن Streamlit Community Cloud يعتمد عليه لمعرفة مكتبات التطبيق، وإذا لم يكن موجوداً فقد يتم تشغيل التطبيق ببيئة فيها Streamlit فقط واعتمادياته الأساسية. 

---

# 12) اختبار محلي قبل الرفع

داخل مجلد المشروع شغّل:

```bash
pip install -r requirements.txt
streamlit run app.py
```

ثم افحص الصفحات التالية:

```text
Market
AI Signals
Portfolio
Africa Impact
Watchlist & Alerts
Whitepaper
Community
Tokenomics & Roadmap
Launch Checklist
Admin
```

إذا ظهرت مشكلة، غالباً ستكون واحدة من هذه:

1. ملف ناقص داخل `src`.
2. دالة غير مضافة في `db.py`.
3. خطأ في اسم صفحة.
4. `ADMIN_PASSWORD` غير موجود عند فتح Admin.
5. اتصال Binance محجوب مؤقتاً أو غير متاح في منطقتك.

---

# 13) قبل الرفع: الشكل النهائي للمشروع

يجب أن يكون عندك تقريباً:

```text
baya_empire/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── .streamlit/
│   └── config.toml
│
├── src/
│   ├── __init__.py
│   ├── auth.py
│   ├── charts.py
│   ├── config.py
│   ├── data.py
│   ├── db.py
│   ├── indicators.py
│   ├── signals.py
│   └── ui.py
│
└── pages/
    ├── 1_Market.py
    ├── 2_AI_Signals.py
    ├── 3_Portfolio.py
    ├── 4_Africa_Impact.py
    ├── 5_Watchlist_Alerts.py
    ├── 6_Whitepaper.py
    ├── 7_Admin.py
    ├── 8_Community.py
    ├── 9_Tokenomics_Roadmap.py
    └── 10_Launch_Checklist.py
```

---

# 14) الرفع إلى GitHub

نفّذ هذه الأوامر داخل مجلد المشروع:

```bash
git init
git add .
git commit -m "Initial Baya Empire Pro MVP"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/baya-empire-pro.git
git push -u origin main
```

استبدل:

```text
YOUR_USERNAME
```

باسم حسابك في GitHub.

---

# 15) النشر على Streamlit Cloud

Streamlit Community Cloud ينشر التطبيقات من GitHub؛ تحتاج ربط حساب GitHub واختيار المستودع والفرع وملف التشغيل الرئيسي، مثل `app.py`. وثائق Streamlit توضّح أن النشر يعتمد على GitHub repository + branch + main file path. 

عند النشر اختر:

```text
Repository: baya-empire-pro
Branch: main
Main file path: app.py
```

ثم من **Advanced settings / Secrets** أضف:

```toml
ADMIN_PASSWORD = "ضع_كلمة_مرور_قوية_هنا"
```

Streamlit يوصي بإدارة الأسرار عبر Secrets بدلاً من وضعها داخل الكود، ويمكن إضافة محتوى `secrets.toml` من إعدادات النشر المتقدمة في Community Cloud. 

---

# 16) بعد النشر مباشرة

بعد أن تحصل على رابط التطبيق:

1. افتح التطبيق من الرابط.
2. جرّب كل الصفحات.
3. افتح صفحة Admin.
4. تأكد أن كلمة المرور تعمل.
5. جرّب إضافة مشروع.
6. جرّب التصويت.
7. جرّب Portfolio.
8. جرّب Watchlist.
9. تأكد أن الصفحة Public إذا تريد نشرها للناس.

Streamlit يتيح مشاركة التطبيق بعد النشر سواء كان عاماً أو خاصاً، ويمكن إرسال دعوات أو مشاركة التطبيق حسب إعدادات المشاركة. 

---

# 17) ملاحظة مهمة قبل الانتشار

حالياً المنصة ممتازة كـ **MVP تجريبي**، لكن قبل انتشار واسع يجب لاحقاً ترقية:

```text
SQLite → Supabase / PostgreSQL
```

لأن قاعدة SQLite المحلية مناسبة للتجربة، لكنها ليست أفضل حل لمنصة فيها مستخدمون حقيقيون، تصويت دائم، وسجلات يجب حفظها باستمرار.

---

## الخطوة التالية

الآن عندك مساران:

### المسار 1: نرفع الآن MVP

نختبر محلياً، نرفع GitHub، ثم Streamlit.

### المسار 2: نضيف Supabase قبل الرفع

هذا أفضل لو تريد بيانات دائمة ومستخدمين حقيقيين.

أنصحك الآن بـ:

```text
نرفع MVP أولاً → نختبر الرابط → ثم نطوّر Supabase في النسخة التالية
```

أرسل لي إذا ظهر لك أي خطأ أثناء التشغيل المحلي أو أثناء الرفع، وسأصلحه لك خطوة بخطوة.
