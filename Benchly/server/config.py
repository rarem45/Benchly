"""Server configuration for Benchly."""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database configuration
DATABASE_PATH = os.getenv("BENCHLY_DB_PATH", os.path.join(BASE_DIR, "benchly.db"))
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATABASE_PATH}")

# Flask settings
FLASK_HOST = os.getenv("BENCHLY_HOST", "0.0.0.0")
# Replit and many hosts set PORT; fall back to our own config var when needed.
FLASK_PORT = int(os.getenv("PORT", os.getenv("BENCHLY_PORT", "5000")))
FLASK_DEBUG = os.getenv("BENCHLY_DEBUG", "False").lower() in ("1", "true", "yes")
