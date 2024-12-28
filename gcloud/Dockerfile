# Use a lightweight Python image
FROM python:3.11-slim

# Install CA certificates and required dependencies
RUN apt-get update && apt-get install -y \
    ca-certificates \
    && update-ca-certificates

# Set the working directory in the container
WORKDIR /app

# Copy the local code to the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir pymongo requests flask

# Expose the default port for Flask
EXPOSE 8080

# Run the Flask app
CMD ["python", "main.py"]