FROM python:3.11-slim

# Set a working directory
WORKDIR /app

# Install system dependencies required by some Python packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       git \
       curl \
       ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . /app

# Expose nothing in particular; the script runs locally.

# Default environment variables (user should override GEMINI_API_KEY at runtime)
ENV PYTHONUNBUFFERED=1

# Default command - run the experiment (user may override)
CMD ["python", "run_experiment.py"]
