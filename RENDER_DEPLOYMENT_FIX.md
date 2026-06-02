# Render Deployment Fix: Dashboard Override Trap

Render has incorrectly auto-detected this repository as a Rust project and is trying to run `cargo build --release`, failing because there is no `Cargo.toml` in the root directory.

Because this is a monorepo with separate `backend` (Python) and `frontend` (Node) directories, Render's auto-detection failed, and it is likely falling back to default behavior based on some dashboard settings that override `render.yaml`.

**To fix this issue:**
1. Go to the Render Dashboard for this specific service.
2. Navigate to **Settings -> Build & Deploy**.
3. Update the **Root Directory** setting to either `backend` or `frontend` depending on which service this deployment is meant for.
4. Ensure the **Build Command** and **Start Command** match the framework in that directory (e.g. `pip install -r requirements.txt && alembic upgrade head` for backend, `npm install && npm run build` for frontend).
5. Trigger a manual deploy.
Dummy update to force commit 1
