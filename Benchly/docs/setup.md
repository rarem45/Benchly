# Benchly Setup Guide

## 1) Create a Python environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 2) Start the server

```powershell
python -m server.app
```

The server listens on `http://127.0.0.1:5000` by default.

## 3) Run the client

```powershell
python -m client.benchly_client --server http://127.0.0.1:5000
```

This runs the benchmarks and submits the results once.

### Running on a schedule

To run Benchly daily, you can use Task Scheduler (Windows) or a cron job (Linux/macOS) and run the same command periodically.

## 4) Run the admin UI

```powershell
python admin/benchly_admin.py --server http://127.0.0.1:5000
```

## 5) Open the web frontend

Open `web/index.html` in your browser and provide the server URL.

## Packaging into executables

To create a single-file Windows executable:

```powershell
pip install pyinstaller
pyinstaller --onefile client/benchly_client.py
pyinstaller --onefile admin/benchly_admin.py
```

The outputs will be in `dist/`.
