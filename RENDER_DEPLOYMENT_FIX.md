# Render Deployment Fix

The recent deployment failed with an error message indicating that Render was attempting to build a Rust project:

`error: could not find 'Cargo.toml' in '/opt/render/project/src' or any parent directory`

This is a known issue: "Dashboard Override Trap: Render Dashboard settings override `render.yaml`. If Render incorrectly auto-detects the monorepo as a Rust project (causing 'Cargo.toml not found' errors), instruct the user to manually update the 'Root Directory' in the Render Dashboard 'Build & Deploy' settings to either `backend` or `frontend`."

## Action Required

To resolve this issue, you must manually update the Root Directory setting in the Render Dashboard:

1. Log in to your Render Dashboard.
2. Select your application service.
3. Go to **Settings** -> **Build & Deploy**.
4. Update the **Root Directory** field. Since this is a monorepo, set it to either `backend` or `frontend`, depending on which part of the application this specific service is intended to run.
5. Trigger a manual deploy.
