# Benchly Overview

Benchly is a modular benchmarking ecosystem for collecting and visualizing PC performance stats.

## Components

- **Client**: Runs on user machines and runs benchmarks (CPU, RAM, disk), then submits JSON results to a Benchly server.
- **Server**: A lightweight Flask API that stores submissions in SQLite, and exposes a leaderboard endpoint.
- **Admin**: A PyQt6 desktop GUI that fetches data from the server and allows administrators to browse and sort results.
- **Web Frontend**: Optional static dashboard that displays the latest results and shop summary.

## Extensibility

Benchly is designed to be extended in the following ways:

- Add more benchmark tests in `client/benchmarks.py` (GPU tests, network tests, etc.)
- Add new API routes in `server/app.py` (e.g. per-machine history, comparisons, metrics)
- Upgrade the admin UI with charts, filtering, and export features using `admin/benchly_admin.py`
- Enhance the web frontend with charts, authentication, or public leaderboards.
