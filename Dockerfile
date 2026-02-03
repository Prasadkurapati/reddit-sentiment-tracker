FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY . .

# Expose ports
EXPOSE 8000 8501

# Run both services (API + Dashboard)
CMD uvicorn app.main:app --host 0.0.0.0 --port 8000 & streamlit run app/dashboard.py --server.port 8501 --server.address 0.0.0.0
