# Render Deployment Fix

The recent deployment failure was caused by Render incorrectly auto-detecting the monorepo as a Rust project. It attempted to run `cargo build --release` but failed because there is no `Cargo.toml`.

**To fix this issue, you must manually update the Render Dashboard:**
1. Open the Render Dashboard and navigate to your service.
2. Go to **Settings -> Build & Deploy**.
3. Update the **Root Directory** to either `backend` or `frontend`, depending on the specific service you are deploying.

Please make this change directly in the dashboard, as it overrides the configuration in `render.yaml`.
