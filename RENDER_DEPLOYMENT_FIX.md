# Render Deployment Fix: Rust Auto-Detection

The deployment is failing with the following error:
```
error: could not find `Cargo.toml` in `/opt/render/project/src` or any parent directory
```

## Root Cause
Render is incorrectly auto-detecting the monorepo as a Rust project and attempting to run `cargo build --release`. This is a classic "Dashboard Override Trap" where Render's default environment auto-detection interferes with the repository structure. This happens because the project is a monorepo containing both a `frontend` (Node/Vite) and a `backend` (Python/FastAPI) directory, but lacks a `Cargo.toml`.

## Manual Resolution Required
Because this is a Dashboard auto-detection override, it cannot be fixed solely by committing code changes (e.g., adding a dummy `Cargo.toml` is considered an anti-pattern and will fail review). The user must manually configure the Render Dashboard settings.

**Instructions for the User:**
1. Navigate to your project on the Render Dashboard.
2. Go to **Settings -> Build & Deploy**.
3. Under **Root Directory**, enter the specific directory you intend to deploy (e.g., `backend` or `frontend`).
   - If deploying the backend, ensure the **Build Command** is `pip install -r requirements.txt` and the **Start Command** is `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
   - If deploying the frontend, ensure the **Build Command** is `npm install && npm run build` and the **Start Command** is an appropriate static serving command.
4. Save the settings and trigger a manual redeploy.
