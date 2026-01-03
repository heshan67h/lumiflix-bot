# Use Python 3.11 official image with all system libraries
FROM python:3.11-slim

# Install system dependencies including SQLite
RUN apt-get update && apt-get install -y \
    libsqlite3-0 \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy bot script
COPY movieverse_bot.py .

# Run the bot
CMD ["python", "movieverse_bot.py"]
