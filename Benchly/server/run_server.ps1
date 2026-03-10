# Run Benchly server (Windows PowerShell)
# Usage: .\run_server.ps1

$env:PORT = $env:PORT -or "5000"
$env:BENCHLY_DB_PATH = $env:BENCHLY_DB_PATH -or (Join-Path $PSScriptRoot "benchly.db")

python -m server.app
