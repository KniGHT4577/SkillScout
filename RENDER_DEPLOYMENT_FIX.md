# Render Deployment Fix

The recent deployment to Render failed with the following error:
`error: could not find 'Cargo.toml' in '/opt/render/project/src' or any parent directory`

This occurred because Render incorrectly auto-detected the project environment as a Rust application rather than correctly identifying the monorepo structure (Python backend or React frontend).

This is a **Dashboard Override Trap**. The settings in the Render Dashboard override the configurations specified in `render.yaml`.

To fix this issue, you must manually update the settings in the Render Dashboard:

1. Go to the **Render Dashboard**.
2. Select the affected service.
3. Navigate to **Settings** -> **Build & Deploy**.
4. Update the **Root Directory** field to point to the correct sub-directory for this service (e.g., `backend` or `frontend`).
5. Ensure the **Build Command** and **Start Command** are set correctly for that environment (e.g., `pip install -r requirements.txt` for backend, `npm install && npm run build` for frontend).
6. Trigger a manual deploy.
