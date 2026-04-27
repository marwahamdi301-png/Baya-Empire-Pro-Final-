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
