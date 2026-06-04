# Render Deployment Fix

The deployment is failing because Render is auto-detecting this project as a Rust application (`cargo build --release`) and looking for `Cargo.toml`. This is a known issue called the "Render Dashboard Override Trap" where dashboard settings override `render.yaml`.

To fix this:
1. Go to the Render Dashboard for your service.
2. Navigate to **Settings -> Build & Deploy**.
3. Update the **Root Directory** setting to either `backend` or `frontend`, depending on which service this deployment is for.
