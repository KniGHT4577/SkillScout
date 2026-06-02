# Fixing Render Deployment: "Cargo.toml not found"

## The Issue
Your Render deployment failed with a Rust build error (`error: could not find 'Cargo.toml'`).
Because this is a monorepo containing both a `frontend` and a `backend` directory, deploying the root directory without explicitly telling Render which sub-directory to build causes Render's auto-detection to fall back to Rust.

## The Fix
You need to update your **Render Dashboard** settings to specify the correct Root Directory for your web service.

1. Go to your Render Dashboard: https://dashboard.render.com
2. Select your failing Web Service.
3. Go to **Settings** -> **Build & Deploy**.
4. Find the **Root Directory** setting.
5. Change it to `backend` (if deploying the Python API) or `frontend` (if deploying the React UI).
6. Click **Save Changes**.
7. Render will automatically start a new deploy using the correct directory context.

*(Note: If you intended to use the `render.yaml` Blueprint, ensure you created a "Blueprint Instance" rather than a standard "Web Service" so that the config is automatically applied).*
