FROM python:3.11-slim

WORKDIR /app

# Install system dependencies required for Playwright and other packages
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install --with-deps chromium

COPY . .

# Expose dynamic port for Cloud Run
ENV PORT=8080

# Make entrypoint executable
RUN chmod +x docker-entrypoint.sh

CMD ["./docker-entrypoint.sh"]
