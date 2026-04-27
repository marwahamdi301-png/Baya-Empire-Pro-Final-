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
