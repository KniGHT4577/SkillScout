# Render Deployment Fix

The repeated deployment failures showing \`could not find 'Cargo.toml'\` are caused by the **Render Dashboard Override Trap**.

Render is ignoring the configuration in \`render.yaml\` and is instead using dashboard-level settings that falsely identify this project (a Python/Node monorepo) as a Rust application.

**You must manually clear these overrides in your Render Dashboard:**

1. Log in to your Render Dashboard.
2. Navigate to your \`skillscout-backend\` and \`skillscout-frontend\` services.
3. Click on **Settings**.
4. In the **Build & Deploy** section, ensure the following fields are **cleared/empty** so that \`render.yaml\` can take effect:
   - Build Command
   - Start Command
   - Root Directory
   - Language / Environment (Should rely on \`render.yaml\` if possible, or explicitly set to Python/Node respectively)
5. Save your settings and trigger a manual deploy.

*Note: The frontend builds successfully in \`NODE_ENV=production\` mode locally without devDependency issues. The failure is entirely due to the incorrect build environment being triggered.*
