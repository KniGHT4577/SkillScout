# Render Deployment Notice

If you encounter a build failure on Render mentioning Rust or Cargo (e.g. `info: downloading 6 components` for `stable-x86_64-unknown-linux-gnu`), this is because Render is falling back to default language detection in the root directory instead of using `render.yaml`.

To fix this:
1. Go to your Render Dashboard.
2. Select your service.
3. Go to **Settings** -> **Build & Deploy**.
4. Set the **Root Directory** explicitly to `frontend` or `backend` depending on the service.

The dashboard settings override `render.yaml`, so this must be done manually if the service was not created correctly via the blueprint.
