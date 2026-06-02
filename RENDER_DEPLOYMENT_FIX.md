# Render Deployment Fix

The Render deployment failed because Render incorrectly auto-detected the project as a Rust application and tried to run `cargo build --release`, looking for a `Cargo.toml`.

Because this is a monorepo (with a `frontend` and `backend` directory), Render needs to be explicitly told which directory to build and deploy from. Dashboard settings override the `render.yaml` configuration in some cases.

**Manual Action Required:**
To fix this deployment error, please manually update the "Root Directory" in the Render Dashboard:
1. Go to your Render Dashboard.
2. Select your service.
3. Navigate to **Settings** -> **Build & Deploy**.
4. Change the **Root Directory** from the default (blank or `/`) to either `frontend` or `backend`, depending on which service this is.
5. Save the changes and trigger a manual deploy.
\n* Update to trigger new commit
