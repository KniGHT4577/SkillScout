# Render Deployment Fix

The deployment failed because Render incorrectly auto-detected the project as a Rust application and tried to run `cargo build --release`, but no `Cargo.toml` exists.

To fix this:
1. Go to the Render Dashboard.
2. Navigate to your project settings (**Settings -> Build & Deploy**).
3. Update the **Root Directory** to point to the correct application folder (e.g., `backend` or `frontend`).
4. Ensure the **Build Command** and **Start Command** are correctly set for Python/FastAPI (for the backend) or Node/Vite (for the frontend).
