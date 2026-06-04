# Render Deployment Fix

The Render deployment failed because Render incorrectly auto-detected the monorepo as a Rust project and tried to run `cargo build --release`, failing because it couldn't find `Cargo.toml`.

To fix this, please manually update the 'Root Directory' in the Render Dashboard 'Build & Deploy' settings to either `backend` or `frontend`.
