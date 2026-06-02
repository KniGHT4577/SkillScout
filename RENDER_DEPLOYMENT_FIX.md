# Render Deployment Fix

The deployment failed because Render incorrectly auto-detected the project as a Rust project, looking for a `Cargo.toml` file.

To fix this, you need to manually configure the Root Directory in the Render Dashboard:

1. Go to the Render Dashboard and select your Web Service.
2. Navigate to **Settings** -> **Build & Deploy**.
3. Set the **Root Directory** to `frontend` (or `backend`, depending on which service is being deployed).
4. Save the changes and trigger a manual deploy.
