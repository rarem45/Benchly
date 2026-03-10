"""Database helpers for Benchly server.

This module supports both SQLite (local file) and SQL database servers via SQLAlchemy.
The database connection is configured via `DATABASE_URL`.
"""

from datetime import datetime
from typing import Any, Dict, List

from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Table,
                        create_engine, func, select)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.engine import Engine
from sqlalchemy.sql import text

from .config import DATABASE_URL


_metadata = MetaData()

_benchmarks = Table(
    "benchmarks",
    _metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("machine_id", String, nullable=False, index=True),
    Column(
        "payload",
        JSONB().as_generic() if DATABASE_URL.startswith("postgres") else String,
        nullable=False,
    ),
    Column("created_at", DateTime, nullable=False),
)


def _get_engine() -> Engine:
    return create_engine(DATABASE_URL, future=True)


def init_db() -> None:
    """Initialize the database and create required tables."""
    engine = _get_engine()
    _metadata.create_all(engine)


def _row_to_record(row: Any) -> Dict[str, Any]:
    payload = row.payload
    # Some DBs may return strings for JSON; attempt to decode if needed
    if isinstance(payload, str):
        try:
            import json

            payload = json.loads(payload)
        except Exception:
            pass

    created_at = row.created_at
    if isinstance(created_at, datetime):
        created_at = created_at.isoformat()

    return {
        "id": row.id,
        "machine_id": row.machine_id,
        "payload": payload,
        "created_at": created_at,
    }


def insert_benchmark(machine_id: str, payload: Dict[str, Any]) -> int:
    """Insert a new benchmark record."""
    engine = _get_engine()
    with engine.begin() as conn:
        result = conn.execute(
            _benchmarks.insert().values(
                machine_id=machine_id,
                payload=payload,
                created_at=datetime.utcnow(),
            )
        )
        return int(result.inserted_primary_key[0])


def get_history(machine_id: str, limit: int = 100) -> List[Dict[str, Any]]:
    """Return historical benchmark entries for a given machine."""
    from .scoring import annotate_with_score

    engine = _get_engine()
    with engine.connect() as conn:
        stmt = (
            select(_benchmarks)
            .where(_benchmarks.c.machine_id == machine_id)
            .order_by(_benchmarks.c.created_at.desc())
            .limit(limit)
        )
        rows = conn.execute(stmt).fetchall()

    records = [_row_to_record(r) for r in rows]
    return [annotate_with_score(r) for r in records]


def get_leaderboard(limit: int = 100, offset: int = 0) -> Dict[str, Any]:
    """Return latest benchmark per machine ordered by score (higher is better)."""
    from .scoring import annotate_with_score

    engine = _get_engine()
    with engine.connect() as conn:
        total = conn.execute(select(func.count(func.distinct(_benchmarks.c.machine_id)))).scalar() or 0

        subq = (
            select(
                _benchmarks.c.machine_id,
                func.max(_benchmarks.c.created_at).label("max_created"),
            )
            .group_by(_benchmarks.c.machine_id)
            .subquery()
        )

        stmt = (
            select(_benchmarks)
            .join(
                subq,
                (subq.c.machine_id == _benchmarks.c.machine_id)
                & (subq.c.max_created == _benchmarks.c.created_at),
            )
        )

        rows = conn.execute(stmt).fetchall()

    records = [_row_to_record(r) for r in rows]
    scored = [annotate_with_score(r) for r in records]
    scored.sort(key=lambda r: r.get("score", 0), reverse=True)

    for idx, entry in enumerate(scored, start=1):
        entry["rank"] = idx

    return {"results": scored[offset : offset + limit], "total": total}
