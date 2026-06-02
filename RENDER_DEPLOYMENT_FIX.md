# Render Deployment Fix

Render incorrectly auto-detected the SkillScout monorepo as a Rust project and attempted to build it using Cargo, which failed because there is no `Cargo.toml`.

This is a known issue called the **Dashboard Override Trap**.

## How to Fix:
1. Open your project on the Render Dashboard.
2. Go to **Settings** -> **Build & Deploy**.
3. Change the **Root Directory** setting manually to `backend` (or `frontend`, depending on which service you are deploying).

This manual override is required to bypass Render's auto-detection.
