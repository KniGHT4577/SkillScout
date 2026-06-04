# Render Deployment Fix: Rust Auto-Detection Dashboard Override Trap

The recent deployment failed with the error `could not find 'Cargo.toml'`. This is a known issue where Render incorrectly auto-detects the monorepo as a Rust project due to the Dashboard overriding `render.yaml` settings.

**Manual Action Required:**
You must manually update the Root Directory in the Render Dashboard to fix this.
1. Go to your Render Dashboard.
2. Select your service.
3. Go to **Settings** → **Build & Deploy**.
4. Update the **Root Directory** setting to either `backend` or `frontend` (depending on which service this is for).
5. Ensure the Build Command and Start Command match what is in `render.yaml` for that service.
6. Trigger a manual deploy.
