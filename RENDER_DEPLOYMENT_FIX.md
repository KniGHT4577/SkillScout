# Render Deployment Fix

The recent deployment failure in Render (Cargo.toml not found) was due to Render incorrectly auto-detecting the monorepo root as a Rust project.

To fix this, you need to manually update the 'Root Directory' in the Render Dashboard 'Build & Deploy' settings to the correct directory (e.g., `backend` or `frontend`), as Dashboard settings override `render.yaml`.
