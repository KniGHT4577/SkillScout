# Render Deployment Fix: Rust Auto-Detection Error

The Render deployment failed because Render incorrectly auto-detected this project as a Rust project and attempted to run `cargo build --release`.
The logs show: `error: could not find 'Cargo.toml' in '/opt/render/project/src' or any parent directory`.

Since this is a monorepo consisting of a FastAPI backend and a React frontend, it does not use Rust.
This is known as the "Dashboard Override Trap", where Render's default environment detection or Dashboard settings override the configurations in `render.yaml`.

## How to Fix

You must manually update your Render Dashboard settings.
Please follow these steps:

1. Log into your Render Dashboard.
2. Navigate to your specific service (Web Service or Static Site).
3. Go to **Settings** -> **Build & Deploy**.
4. Update the **Root Directory** setting:
   - For the backend service, set the Root Directory to `backend`.
   - For the frontend service, set the Root Directory to `frontend`.
5. Ensure the Build Command and Start Command match the project type:
   - **Backend**:
     - Build Command: `pip install -r requirements.txt && alembic upgrade head`
     - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Frontend**:
     - Build Command: `npm install && npm run build`
     - Start Command: `npx serve -s dist` (or whichever output directory is used)
6. Manually trigger a new deploy.
