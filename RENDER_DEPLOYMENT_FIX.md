# Render Deployment Fix

The Render deployment is failing with "could not find 'Cargo.toml'" because Render is incorrectly auto-detecting the monorepo as a Rust project.

To fix this, you need to manually update the Render Dashboard settings, as Dashboard settings override `render.yaml`.

1. Go to the **Render Dashboard**.
2. Select your service.
3. Go to **Settings -> Build & Deploy**.
4. Update the **Root Directory** to either `backend` or `frontend` depending on which service is failing.
5. Save the changes and trigger a manual deploy.
