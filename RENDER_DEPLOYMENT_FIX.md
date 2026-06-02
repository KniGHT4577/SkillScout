# Render Deployment Fix

The Render deployment failed because Render incorrectly auto-detected the project as a Rust project and tried to run `cargo build --release` (which failed due to the missing `Cargo.toml`).

This is a known issue called the "Dashboard Override Trap". Since this project is a monorepo containing both a `frontend` (React/Vite) and `backend` (FastAPI), Render's auto-detection needs to be manually corrected in the dashboard.

## Manual Steps Required

Please follow these steps in the Render Dashboard to resolve the deployment issue:

1. Go to the **Render Dashboard**.
2. Select your service.
3. Go to **Settings -> Build & Deploy**.
4. Change the **Root Directory** from the default (which is the repository root) to either `backend` or `frontend`, depending on which service this specific Render instance is meant to deploy.
5. Manually trigger a new deploy.
