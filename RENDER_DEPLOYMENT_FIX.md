# Render Deployment Instructions
The deployment failed with 'Cargo.toml not found' because Render incorrectly auto-detected this monorepo as a Rust project.
The Render Dashboard settings are overriding the configurations defined in 'render.yaml'.

**YOU MUST MANUALLY CLEAR THE DASHBOARD OVERRIDES SO THAT 'render.yaml' IS RESPECTED.**

1. Go to your Render Dashboard (https://dashboard.render.com).
2. Select the failing service.
3. Go to **Settings -> Build & Deploy**.
4. Clear the **Root Directory** field, or ensure it is correctly set to 'backend' (for the API) or 'frontend' (for the static site).
5. Ensure the Build Command and Start Command are not overridden. Look for the 'Clear' button next to them and click it if it exists.
6. Check **Settings -> Language/Environment** and ensure it's not set to Rust if possible, though clearing the root directory usually fixes the auto-detect issue.
7. Save the changes and retry the deploy.

