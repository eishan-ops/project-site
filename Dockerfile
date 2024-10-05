# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install Nginx and other dependencies
RUN apt-get update && apt-get install -y nginx supervisor && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages
RUN pip install --no-cache-dir fastapi uvicorn gunicorn boto3

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copy static files
COPY index.html /usr/share/nginx/html/
COPY background.jpg /usr/share/nginx/html/

# Create necessary directories
RUN mkdir -p /var/log/fastapi /var/run/supervisor

# Make port 80 available to the world outside this container
EXPOSE 80

# Run supervisord
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]