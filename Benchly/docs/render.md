# Deploy Benchly on Render

This guide shows how to deploy the Benchly server on Render (https://render.com). Render can build your app from the included `Dockerfile` and run it as a public web service.

---

## 1) Create a new Render Web Service

1. Go to https://dashboard.render.com and log in.
2. Click **New** → **Web Service**.
3. Select your Benchly GitHub/GitLab repository.
4. Set the **Name** (e.g., `benchly`).
5. Choose **Environment**: `Docker`.
6. Leave **Build Command** empty (Render will use the `Dockerfile`).
7. Ensure **Start Command** is blank (Docker image already specifies `CMD`).
8. Choose a plan (Free/Starter is fine for evaluation).

---

## 2) Ensure the server binds to the correct port

Render provides a `PORT` environment variable. Benchly already respects this via `server/config.py` (it falls back to `PORT`, then `BENCHLY_PORT`).

If you want to explicitly set a port, add an environment variable in Render:

- `PORT` = `5000` (optional)

---

## 3) (Optional) Use a managed database

Render can provision a PostgreSQL database. If you want persistent storage across deploys and restarts, do the following:

1. In the Render dashboard, under **New** → **PostgreSQL Database**, create a database.
2. Copy the `DATABASE_URL` from the database dashboard.
3. In your Benchly Web Service settings, add an environment variable:
   - `DATABASE_URL` = `<value from Render>`

Benchly will use `DATABASE_URL` automatically.

> ⚠️ Note: If you do not set `DATABASE_URL`, Benchly will use a local SQLite database at `server/benchly.db`. Render’s filesystem is ephemeral, so data will be lost on redeploys.

---

## 4) Deploy

Render will build your service and deploy it automatically after you connect the repo. Once deployed, your service will be available at a public URL like:

```
https://<your-service>.onrender.com
```

---

## 5) Point clients at your Render server

```powershell
python -m client.benchly_client --server https://<your-service>.onrender.com
```

---

## Optional: `render.yaml` (Infrastructure-as-Code)

If you want to store Render configuration in source control, you can add a `render.yaml` file to the repo root. This file is optional and can be used to configure the service and environment variables.

Example (replace `<your-repo>` and `<branch>` appropriately):

```yaml
services:
  - type: web
    name: benchly
    env: docker
    plan: free
    repo: <your-repo>
    branch: main
    dockerfilePath: Dockerfile
    envVars:
      - key: PORT
        value: "5000"
      # - key: DATABASE_URL
      #   value: "postgres://..."
```
