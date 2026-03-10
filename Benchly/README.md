# Benchly

Benchly is a modular benchmarking ecosystem for measuring, collecting, and visualizing PC performance data.

## Components

- **Client**: Runs on user machines, detects hardware, runs benchmarks (CPU, RAM, disk), and submits results to the server.
- **Server**: REST API + SQLite storage for submissions and leaderboard retrieval.
- **Admin**: Desktop GUI (PyQt6) for fetching and visualizing benchmark data.
- **Web Frontend**: Optional static website that consumes the server API.

## Quick Start

### 1) Setup Python environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2) Start the server

```powershell
python -m server.app
```

The server will start on `http://127.0.0.1:5000` by default.

### 3) Run the client (one-time benchmark)

```powershell
python -m client.benchly_client --server http://127.0.0.1:5000
```

### 4) Run the admin GUI

```powershell
python -m admin.benchly_admin --server http://127.0.0.1:5000
```

### 5) Optional: Open the web dashboard

Open `web/index.html` in a browser (or serve it over a local server) and it will fetch data from the server.

### 6) Deploy on Replit (public server)

Benchly can be hosted on Replit so other machines can submit benchmarks over the internet.

1. Create a new Replit (Python) and upload this repo.
2. Ensure `requirements.txt` is present; Replit will install it automatically.
3. In `Secrets`, you can optionally set `BENCHLY_PORT` or `BENCHLY_DEBUG`.
4. Run (Replit will start the server and expose it via a public URL).

Your clients can then point at:

```
https://<your-replit-name>.repl.co
```

## Leaderboard & Ranking

Benchly computes a simple **score** for each submission by normalizing benchmark times and combining them into a single value (higher is better). The API `/leaderboard` endpoint returns sorted results by score.

- `GET /leaderboard` returns the top results (highest score first)
- Supports query params:
  - `limit` (default `100`)
  - `offset` (default `0`)

Example:

```powershell
curl "http://127.0.0.1:5000/leaderboard?limit=50&offset=0"
```

The JSON response includes:

- `results`: list of benchmark entries with `score` and `rank`
- `count`: number of results returned
- `total`: total unique machines in the database


## Packaging into Executables

Benchly can be packaged using [PyInstaller](https://www.pyinstaller.org/):

```powershell
pip install pyinstaller
pyinstaller --onefile client/benchly_client.py
pyinstaller --onefile admin/benchly_admin.py
```


## Project Structure

- `client/` - Client benchmark runner
- `server/` - Flask REST server + SQLite database
- `admin/` - PyQt6 desktop admin GUI
- `web/` - Optional web frontend (HTML/JS)
- `shared/` - Common helper code and constants
- `configs/` - Default configuration files
- `docs/` - Documentation and usage guides
- `releases/` - Packaged executables or release artifacts
