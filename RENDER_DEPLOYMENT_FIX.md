# Render Deployment Instructions
The deployment failed with 'Cargo.toml not found' because Render incorrectly auto-detected this monorepo as a Rust project.
To fix this, you must manually clear the Dashboard Overrides so that 'render.yaml' is respected.

1. Go to your Render Dashboard (https://dashboard.render.com).
2. Select the failing service.
3. Go to **Settings -> Build & Deploy**.
4. Clear the **Root Directory** field, or ensure it is correctly set to 'backend' (for the API) or 'frontend' (for the static site).
5. Ensure the Build Command and Start Command are not overridden.
6. Save the changes and retry the deploy.

