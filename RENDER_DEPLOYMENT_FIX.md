# Render Deployment Fix
The project deployment has failed because Render auto-detected the repository as a Rust project and attempted to build it using Cargo (`cargo build --release`), leading to a `could not find Cargo.toml` error.

This is a known issue called the "Dashboard Override Trap", where Render's auto-detection incorrectly overrides the settings in `render.yaml`.

This requires a manual fix in the Render Dashboard. You must change the "Root Directory" to either `backend` or `frontend` depending on the service you are trying to deploy, so Render can correctly auto-detect the environment (Python or Node.js) and build tools.
Manual change needed
