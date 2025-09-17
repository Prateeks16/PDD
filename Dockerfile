# Use Python 3.12 base image
FROM python:3.12-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose port 8080 for Render
EXPOSE 8080

# Start the API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
