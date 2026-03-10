# Benchly server Docker image
# Builds a minimal environment to run the Benchly Flask API.

FROM python:3.14-slim

WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure the database directory exists
RUN mkdir -p /app/server

# Expose the default Benchly port
EXPOSE 5000

# Run the server (port can be overridden via PORT env var)
CMD ["python", "-m", "server.app"]
