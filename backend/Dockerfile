# Start from an official Python image (slim = smaller size, based on Debian Linux)
FROM python:3.12-slim

# Install Pandoc via apt (Linux package manager, like pip but for system tools)
RUN apt-get update && apt-get install -y pandoc && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy and install Python dependencies first (Docker caches this layer — faster rebuilds)
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Tell Render what port we're using
EXPOSE 8000

# Start the server (no --reload in production)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]