def init_db():
    with get_conn() as conn:
        # Portfolio
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS portfolio (
                id INTEGER PRIMARY KEY,
                cash REAL NOT NULL
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS positions (
                symbol TEXT PRIMARY KEY,
                qty REAL NOT NULL,
                avg_price REAL NOT NULL,
                realized_pnl REAL NOT NULL DEFAULT 0
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                side TEXT NOT NULL,
                price REAL NOT NULL,
                amount REAL NOT NULL,
                total REAL NOT NULL,
                fee REAL NOT NULL,
                time TEXT NOT NULL
            )
            """
        )

        # Africa Impact Projects
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                country TEXT NOT NULL,
                name TEXT NOT NULL,
                sector TEXT NOT NULL,
                target REAL NOT NULL,
                raised REAL NOT NULL DEFAULT 0,
                status TEXT NOT NULL,
                description TEXT,
                created_at TEXT NOT NULL
            )
            """
        )

        # Voting
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS project_votes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                voter_key TEXT NOT NULL,
                created_at TEXT NOT NULL,
                UNIQUE(project_id, voter_key)
            )
            """
        )

        # Watchlist
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS watchlist (
                symbol TEXT PRIMARY KEY,
                added_at TEXT NOT NULL
            )
            """
        )

        # Price Alerts
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                condition TEXT NOT NULL,
                target_price REAL NOT NULL,
                active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL,
                triggered_at TEXT
            )
            """
        )

        # Initial Portfolio Cash
        exists = conn.execute(
            "SELECT COUNT(*) FROM portfolio WHERE id = 1"
        ).fetchone()[0]

        if exists == 0:
            conn.execute(
                "INSERT INTO portfolio (id, cash) VALUES (1, ?)",
                (INITIAL_CASH,)
            )

        # Seed Impact Projects
        projects_count = conn.execute(
            "SELECT COUNT(*) FROM projects"
        ).fetchone()[0]

        if projects_count == 0:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            demo_projects = [
                (
                    "كينيا",
                    "طاقة شمسية لمدرسة ريفية",
                    "طاقة / تعليم",
                    12000,
                    3500,
                    "قيد التمويل",
                    "مشروع يهدف إلى توفير ألواح شمسية لمدرسة ريفية لتحسين الوصول للكهرباء والتعليم الرقمي.",
                    now
                ),
                (
                    "السنغال",
                    "دعم تعاونية زراعية للشباب",
                    "زراعة",
                    8000,
                    2100,
                    "قيد التحقق",
                    "دعم تعاونية شبابية عبر معدات بسيطة وتكوين في التسويق الرقمي.",
                    now
                ),
                (
                    "المغرب",
                    "تكوين رقمي للشباب",
                    "تعليم رقمي",
                    5000,
                    1200,
                    "قيد التمويل",
                    "برنامج تدريبي لتعليم أساسيات البرمجة والتسويق الرقمي للشباب.",
                    now
                ),
                (
                    "غانا",
                    "معدات لمركز تدريب مهني",
                    "تكوين / شباب",
                    15000,
                    6000,
                    "قيد التمويل",
                    "دعم مركز تدريب مهني بمعدات عملية للشباب ورواد الأعمال الصغار.",
                    now
                ),
            ]
# =========================
# Africa Impact Projects
# =========================

def get_projects():
    with get_conn() as conn:
        projects = pd.read_sql_query(
            """
            SELECT
                id,
                country,
                name,
                sector,
                target,
                raised,
                status,
                description,
                created_at
            FROM projects
            ORDER BY id DESC
            """,
            conn
        )

        votes = pd.read_sql_query(
            """
            SELECT
                project_id,
                COUNT(*) AS votes
            FROM project_votes
            GROUP BY project_id
            """,
            conn
        )

    if projects.empty:
        return projects

    if votes.empty:
        projects["votes"] = 0
    else:
        projects = projects.merge(
            votes,
            left_on="id",
            right_on="project_id",
            how="left"
        )
        projects["votes"] = projects["votes"].fillna(0).astype(int)
        projects = projects.drop(columns=["project_id"], errors="ignore")

    return projects


def add_project(country, name, sector, target, raised, status, description):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO projects
            (country, name, sector, target, raised, status, description, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                country,
                name,
                sector,
                target,
                raised,
                status,
                description,
                now
            )
        )


def update_project(project_id, raised, status):
    with get_conn() as conn:
        conn.execute(
            """
            UPDATE projects
            SET raised = ?, status = ?
            WHERE id = ?
            """,
            (raised, status, project_id)
        )


def delete_project(project_id):
    with get_conn() as conn:
        conn.execute(
            "DELETE FROM project_votes WHERE project_id = ?",
            (project_id,)
        )
        conn.execute(
            "DELETE FROM projects WHERE id = ?",
            (project_id,)
        )


def vote_project(project_id, voter_key):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with get_conn() as conn:
            conn.execute(
                """
                INSERT INTO project_votes
                (project_id, voter_key, created_at)
                VALUES (?, ?, ?)
                """,
                (project_id, voter_key, now)
            )
        return True, "تم تسجيل تصويتك بنجاح."
    except sqlite3.IntegrityError:
        return False, "لقد صوتّ على هذا المشروع من قبل."


# =========================
# Watchlist
# =========================

def add_to_watchlist(symbol):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_conn() as conn:
        conn.execute(
            """
            INSERT OR IGNORE INTO watchlist
            (symbol, added_at)
            VALUES (?, ?)
            """,
            (symbol, now)
        )


def remove_from_watchlist(symbol):
    with get_conn() as conn:
        conn.execute(
            "DELETE FROM watchlist WHERE symbol = ?",
            (symbol,)
        )


def get_watchlist():
    with get_conn() as conn:
        df = pd.read_sql_query(
            """
            SELECT symbol, added_at
            FROM watchlist
            ORDER BY added_at DESC
            """,
            conn
        )

    if df.empty:
        return []

    return df["symbol"].tolist()


# =========================
# Price Alerts
# =========================

def create_alert(symbol, condition, target_price):
    if condition not in [">=", "<="]:
        return False, "نوع الشرط غير صحيح."

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO alerts
            (symbol, condition, target_price, active, created_at)
            VALUES (?, ?, ?, 1, ?)
            """,
            (symbol, condition, target_price, now)
        )

    return True, "تم إنشاء التنبيه بنجاح."


def get_alerts(active_only=False):
    query = """
        SELECT
            id,
            symbol,
            condition,
            target_price,
            active,
            created_at,
            triggered_at
        FROM alerts
    """

    params = []

    if active_only:
        query += " WHERE active = 1"

    query += " ORDER BY id DESC"

    with get_conn() as conn:
        return pd.read_sql_query(query, conn, params=params)


def deactivate_alert(alert_id):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_conn() as conn:
        conn.execute(
            """
            UPDATE alerts
            SET active = 0, triggered_at = ?
            WHERE id = ?
            """,
            (now, alert_id)
        )


def evaluate_alerts(price_map):
    alerts = get_alerts(active_only=True)
    triggered = []

    if alerts.empty:
        return triggered

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_conn() as conn:
        for _, alert in alerts.iterrows():
            symbol = alert["symbol"]

            if symbol not in price_map:
                continue

            current_price = price_map[symbol]
            target = float(alert["target_price"])
            condition = alert["condition"]

            hit = False

            if condition == ">=" and current_price >= target:
                hit = True

            if condition == "<=" and current_price <= target:
                hit = True

            if hit:
                conn.execute(
                    """
                    UPDATE alerts
                    SET active = 0, triggered_at = ?
                    WHERE id = ?
                    """,
                    (now, int(alert["id"]))
                )

                triggered.append(
                    {
                        "symbol": symbol,
                        "condition": condition,
                        "target_price": target,
                        "current_price": current_price,
                    }
                )

    return triggered
            conn.executemany(
                """
                INSERT INTO projects
                (country, name, sector, target, raised, status, description, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                demo_projects
            )
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
