"""Scoring utilities for Benchly.

Benchly scores are derived from benchmark durations where lower is better.
This module provides a deterministic way to turn raw benchmark timings into
a single "score" value that can be used for sorting and leaderboard ranking.
"""

from __future__ import annotations

from typing import Any, Dict, Optional


# Baseline durations (seconds) used to normalize scores.
# These represent a plausible reference machine.
BASELINE_CPU_S = 2.0
BASELINE_RAM_S = 0.35
BASELINE_DISK_S = 0.55


def _safe_div(numerator: float, denominator: float, fallback: float = 0.0) -> float:
    if denominator is None or denominator <= 0:
        return fallback
    return numerator / denominator


def compute_score(results: Dict[str, Any]) -> float:
    """Compute an overall score from benchmark results.

    The higher the score, the better.

    Score formula:
        score = cpu_score + ram_score + disk_score

    Where each component is normalized by a baseline.
    """

    cpu_dur = float(results.get("cpu", {}).get("duration_s") or 0)
    ram_dur = float(results.get("ram", {}).get("duration_s") or 0)
    disk_write = float(results.get("disk", {}).get("write_seconds") or 0)
    disk_read = float(results.get("disk", {}).get("read_seconds") or 0)

    cpu_score = _safe_div(BASELINE_CPU_S, cpu_dur, fallback=0.0)
    ram_score = _safe_div(BASELINE_RAM_S, ram_dur, fallback=0.0)
    disk_score = _safe_div(BASELINE_DISK_S, disk_write + disk_read, fallback=0.0)

    return cpu_score + ram_score + disk_score


def annotate_with_score(record: Dict[str, Any]) -> Dict[str, Any]:
    """Return a copy of a benchmark record annotated with a calculated score."""
    if not record:
        return record

    payload = record.get("payload") or {}
    results = payload.get("results") or {}
    score = compute_score(results)
    return {**record, "score": score}
