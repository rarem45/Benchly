"""Shared utility helpers for Benchly."""

import json
import logging
import platform
import socket
from datetime import datetime


def configure_basic_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def safe_json_dump(data):
    """Return a JSON string with stable sorting and indentation."""
    return json.dumps(data, sort_keys=True, indent=2)


def get_machine_identity():
    """Return a simple machine identifier dictionary."""
    return {
        "hostname": socket.gethostname(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
