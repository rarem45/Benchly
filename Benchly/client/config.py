"""Client configuration and defaults."""

from pathlib import Path

DEFAULT_SERVER_URL = "http://127.0.0.1:5000"
DEFAULT_RUN_ONCE = True
DEFAULT_RUN_INTERVAL_SECONDS = 24 * 60 * 60

# Disk benchmark uses a temp file inside user home directory
DEFAULT_TEMP_DIR = Path.home() / ".benchly"
DEFAULT_TEMP_DIR.mkdir(parents=True, exist_ok=True)
DEFAULT_DISK_TEST_FILE = DEFAULT_TEMP_DIR / "benchly_disk_test.bin"
