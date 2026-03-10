# Deploy Benchly on Railway

This guide shows the fastest way to deploy Benchly to a public server using Railway.

---

## 1) Install the Railway CLI

On Windows/macOS/Linux:

```bash
npm install -g railway
```

Then authenticate:

```bash
railway login
```

---

## 2) Initialize your project

From the Benchly repo root:

```bash
railway init
```

Choose a project name (or accept the default). Railway will create a `.railway` directory.

---

## 3) Add a PostgreSQL database (recommended)

```bash
railway add
```

Select **PostgreSQL** and follow the prompts.

Railway will automatically add a `DATABASE_URL` env var to your project.

---

## 4) Deploy

```bash
railway up
```

Railway will build the app (it will use the included `Dockerfile` by default) and deploy it.

Once complete, Railway provides a public URL of the form:

```
https://<your-project>.up.railway.app
```

---

## 5) Point clients to the Railway server

```powershell
python -m client.benchly_client --server https://<your-project>.up.railway.app
```

---

## Notes

- Railway automatically sets `PORT`, which Benchly already respects.
- The database is managed by Railway; no extra configuration should be required.
