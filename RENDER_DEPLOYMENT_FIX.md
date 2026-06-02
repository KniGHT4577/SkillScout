# Render Deployment Fix

The Render deployment failed because Render incorrectly auto-detected the project as a Rust project and tried to run `cargo build --release`, failing because there is no `Cargo.toml`.

To fix this, you must manually update the settings in the Render Dashboard:
1. Go to your Render Dashboard.
2. Select your service.
3. Go to **Settings -> Build & Deploy**.
4. Update the **Root Directory** to either `backend` or `frontend` depending on the service you are deploying.
