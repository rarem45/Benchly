# Deploying Benchly Server

This guide shows common ways to run the Benchly server so multiple clients can submit benchmarks.

---

## Option 1: Run locally (Windows)

### 1) Create and activate virtualenv

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2) Start the server

Run either:

```powershell
python -m server.app
```

or (recommended) use the helper script:

```powershell
cd server
.\run_server.ps1
```

The server will listen on `http://127.0.0.1:5000` by default.

---

## Option 2: Run in Docker (recommended for production/test)

### 1) Build the image

```bash
docker build -t benchly:latest .
```

### 2) Run the container

```bash
docker run -p 5000:5000 --name benchly benchly:latest
```

The server will be available on `http://localhost:5000`.

---

## Option 3: Deploy on a cloud host (VPS or PaaS)

### 1) Clone the repo

```bash
git clone <your-repo-url> benchly
cd benchly
```

### 2) Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3) Run the server

```bash
python -m server.app
```

> **Tip:** If the host provides a `PORT` environment variable (e.g., Heroku, Railway, Replit), Benchly will bind to it automatically.

---

## Railway deployment (recommended for public hosting)

See `docs/railway.md` for step-by-step instructions to deploy Benchly on Railway with a managed PostgreSQL database.

---

## Optional: Run as a background service (Linux)

Create a systemd service (`/etc/systemd/system/benchly.service`):

```ini
[Unit]
Description=Benchly server
After=network.target

[Service]
Type=simple
User=<your-user>
WorkingDirectory=/path/to/benchly
ExecStart=/path/to/benchly/.venv/bin/python -m server.app
Restart=always

[Install]
WantedBy=multi-user.target
```

Then enable and start:

```bash
sudo systemctl enable benchly
sudo systemctl start benchly
```

---

## Deploy on Railway (Docker + managed database)

Railway makes it easy to deploy Docker apps and provision managed databases.

### 1) Create a Railway project

- Go to https://railway.app and log in.
- Create a new project and choose **Deploy from GitHub**.
- Connect your Benchly repository.

### 2) Add a PostgreSQL plugin

- In Railway, add the **PostgreSQL** plugin.
- Railway will set a `DATABASE_URL` environment variable automatically.

### 3) Ensure the server binds to the provided port

Railway provides a `PORT` env var. Benchly already uses it by default.

### 4) Deploy

Railway will build and deploy your app (it uses the `Dockerfile` if present).

### 5) Connect clients

After deployment, Railway gives you a public URL like:

```
https://<project-name>.up.railway.app
```

Point clients at that URL:

```powershell
python -m client.benchly_client --server https://<project-name>.up.railway.app
```

---

## How clients connect

Point any client to your server base URL, e.g.:

```powershell
python -m client.benchly_client --server http://<your-host>:5000
```

If your server is public (e.g., `https://benchly.myhost.com`), use that URL.
