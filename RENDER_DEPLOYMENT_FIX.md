# Render Deployment Fix

The Render deployment failed because it incorrectly auto-detected this repository as a Rust project, attempting to run `cargo build --release` when no `Cargo.toml` exists in the root. This is a monorepo containing a frontend and backend.

## Manual Steps Required

To fix this, you must update the Render Dashboard settings for your service:

1. Go to your Render Dashboard (https://dashboard.render.com).
2. Select the service that is failing to deploy.
3. Navigate to **Settings** -> **Build & Deploy**.
4. Update the **Root Directory** setting to either `backend` or `frontend`, depending on which part of the monorepo this service is supposed to deploy.
5. Save the changes and trigger a manual deploy.
