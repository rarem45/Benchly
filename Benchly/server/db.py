"""SQLite helpers for Benchly server."""

import json
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional

from .config import DATABASE_PATH


def _connect():
    conn = sqlite3.connect(DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initialize the database and create required tables."""
    conn = _connect()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS benchmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                machine_id TEXT NOT NULL,
                payload JSON NOT NULL,
                created_at TIMESTAMP NOT NULL
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def insert_benchmark(machine_id: str, payload: Dict[str, Any]) -> int:
    """Insert a new benchmark record."""
    conn = _connect()
    try:
        cursor = conn.execute(
            "INSERT INTO benchmarks (machine_id, payload, created_at) VALUES (?, ?, ?)",
            (machine_id, json.dumps(payload), datetime.utcnow()),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def get_history(machine_id: str, limit: int = 100) -> List[Dict[str, Any]]:
    """Return historical benchmark entries for a given machine."""
    from .scoring import annotate_with_score

    conn = _connect()
    try:
        cursor = conn.execute(
            """
            SELECT id, machine_id, payload, created_at
            FROM benchmarks
            WHERE machine_id = ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (machine_id, limit),
        )
        rows = cursor.fetchall()
        records = [
            {
                "id": row["id"],
                "machine_id": row["machine_id"],
                "payload": json.loads(row["payload"]),
                "created_at": row["created_at"].isoformat() if isinstance(row["created_at"], datetime) else row["created_at"],
            }
            for row in rows
        ]
        return [annotate_with_score(r) for r in records]
    finally:
        conn.close()


def get_leaderboard(limit: int = 100, offset: int = 0) -> Dict[str, Any]:
    """Return latest benchmark per machine ordered by score (higher is better).

    Returns a dictionary with:
      - results: list of benchmark records
      - total: number of unique machines
    """
    from .scoring import annotate_with_score

    conn = _connect()
    try:
        total_cursor = conn.execute("SELECT COUNT(DISTINCT machine_id) AS total FROM benchmarks")
        total = total_cursor.fetchone()["total"]

        cursor = conn.execute(
            """
            SELECT b1.id, b1.machine_id, b1.payload, b1.created_at
            FROM benchmarks b1
            JOIN (
                SELECT machine_id, MAX(created_at) AS max_created
                FROM benchmarks
                GROUP BY machine_id
            ) b2 ON b1.machine_id = b2.machine_id AND b1.created_at = b2.max_created
            """,
        )
        rows = cursor.fetchall()

        records = [
            {
                "id": row["id"],
                "machine_id": row["machine_id"],
                "payload": json.loads(row["payload"]),
                "created_at": row["created_at"].isoformat() if isinstance(row["created_at"], datetime) else row["created_at"],
            }
            for row in rows
        ]

        # Annotate with score and sort descending.
        scored = [annotate_with_score(r) for r in records]
        scored.sort(key=lambda r: r.get("score", 0), reverse=True)

        # Add a stable rank field for clients
        for idx, entry in enumerate(scored, start=1):
            entry["rank"] = idx

        return {"results": scored[offset : offset + limit], "total": total}
    finally:
        conn.close()
