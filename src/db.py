import sqlite3
from datetime import datetime

import pandas as pd

from src.config import DB_NAME, INITIAL_CASH, PAPER_FEE_RATE


def get_conn():
    return sqlite3.connect(DB_NAME, timeout=10)


def init_db():
    with get_conn() as conn:
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

        exists = conn.execute(
            "SELECT COUNT(*) FROM portfolio WHERE id = 1"
        ).fetchone()[0]

        if exists == 0:
            conn.execute(
                "INSERT INTO portfolio (id, cash) VALUES (1, ?)",
                (INITIAL_CASH,)
            )


def get_cash():
    with get_conn() as conn:
        row = conn.execute(
            "SELECT cash FROM portfolio WHERE id = 1"
        ).fetchone()

    return float(row[0]) if row else INITIAL_CASH


def get_positions():
    with get_conn() as conn:
        df = pd.read_sql_query(
            """
            SELECT
                symbol,
                qty,
                avg_price,
                realized_pnl
            FROM positions
            WHERE qty > 0.00000001
            ORDER BY symbol
            """,
            conn
        )

    return df


def get_trades(limit=100):
    with get_conn() as conn:
        df = pd.read_sql_query(
            """
            SELECT
                symbol AS الزوج,
                side AS النوع,
                price AS السعر,
                amount AS الكمية,
                total AS الإجمالي,
                fee AS الرسوم,
                time AS الوقت
            FROM trades
            ORDER BY id DESC
            LIMIT ?
            """,
            conn,
            params=(limit,)
        )

    return df


def execute_trade(symbol, side, price, amount):
    if amount <= 0:
        return False, "الكمية يجب أن تكون أكبر من صفر."

    side = side.upper()
    if side not in ["BUY", "SELL"]:
        return False, "نوع العملية غير صحيح."

    total = price * amount
    fee = total * PAPER_FEE_RATE
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_conn() as conn:
        cash = conn.execute(
            "SELECT cash FROM portfolio WHERE id = 1"
        ).fetchone()[0]

        pos = conn.execute(
            """
            SELECT qty, avg_price, realized_pnl
            FROM positions
            WHERE symbol = ?
            """,
            (symbol,)
        ).fetchone()

        if pos:
            old_qty, old_avg, realized_pnl = pos
        else:
            old_qty, old_avg, realized_pnl = 0.0, 0.0, 0.0

        if side == "BUY":
            cost = total + fee

            if cash < cost:
                return False, "الرصيد الافتراضي غير كافٍ لتنفيذ الشراء."

            new_cash = cash - cost
            new_qty = old_qty + amount

            if new_qty > 0:
                new_avg = ((old_qty * old_avg) + (amount * price)) / new_qty
            else:
                new_avg = 0.0

            new_realized = realized_pnl

        else:
            if old_qty + 1e-12 < amount:
                return False, "لا تملك كمية كافية للبيع في المحفظة الافتراضية."

            proceeds = total - fee
            new_cash = cash + proceeds
            new_qty = old_qty - amount
            trade_pnl = (price - old_avg) * amount - fee
            new_realized = realized_pnl + trade_pnl
            new_avg = old_avg if new_qty > 0.00000001 else 0.0

        conn.execute(
            "UPDATE portfolio SET cash = ? WHERE id = 1",
            (new_cash,)
        )

        conn.execute(
            """
            INSERT INTO positions (symbol, qty, avg_price, realized_pnl)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(symbol) DO UPDATE SET
                qty = excluded.qty,
                avg_price = excluded.avg_price,
                realized_pnl = excluded.realized_pnl
            """,
            (symbol, new_qty, new_avg, new_realized)
        )

        conn.execute(
            """
            INSERT INTO trades (symbol, side, price, amount, total, fee, time)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (symbol, side, price, amount, total, fee, now)
        )

    return True, "تم تنفيذ العملية الورقية بنجاح."


def reset_portfolio():
    with get_conn() as conn:
        conn.execute("DELETE FROM trades")
        conn.execute("DELETE FROM positions")
        conn.execute("DELETE FROM portfolio")
        conn.execute(
            "INSERT INTO portfolio (id, cash) VALUES (1, ?)",
            (INITIAL_CASH,)
        )
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
                )# =========================
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
