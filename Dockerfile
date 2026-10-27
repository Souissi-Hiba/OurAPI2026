# Use a small Python image for the application.
FROM python:3.13-slim

# Keep the application files in one working directory.
WORKDIR /app

# Copy dependencies before application code to reuse Docker's build cache.
COPY requirements.txt .

# Install the pinned dependencies without keeping pip's cache.
RUN pip install --no-cache-dir -r requirements.txt

# Add the Flask application to the image.
COPY app.py .

# Document the port used by Flask.
EXPOSE 5000

# Start Flask on all container network interfaces.
CMD ["flask", "--app", "app", "run", "--host=0.0.0.0", "--port=5000"]
