# Render Deployment Fix

The deployment is failing with the error: `could not find Cargo.toml in /opt/render/project/src or any parent directory`.
This occurs because Render's auto-detection incorrectly identifies this monorepo as a Rust project.

To fix this, you must manually configure the Render Dashboard settings, which override `render.yaml`.

**Instructions:**
1. Go to your Render Dashboard.
2. Select your service.
3. Navigate to **Settings -> Build & Deploy**.
4. Update the **Root Directory** field to either `backend` or `frontend`, depending on the service you are trying to deploy.
5. Save the changes and trigger a manual deploy.
Update: Deployment still failing because Dashboard settings must be manually changed.
