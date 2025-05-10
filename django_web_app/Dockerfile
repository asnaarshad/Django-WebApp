# Use a more secure and updated Python image
# FROM python:3.11-slim # negative case

# Use of vulnerable base image -Positive case
FROM python:3.6  # known to have vulnerabilities

# Set the working directory inside the container
WORKDIR /django_web_app

# Copy the current directory contents into the container
COPY . .

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Running container as root
#Tool: Docker Bench
#Positive Case (Vulnerable) — default Dockerfile runs as root.

# Negative Case (Secure) — run as nonroot:
# Create a non-root user for security purposes
RUN useradd -m nonroot
USER nonroot

# Expose port for the Django app
EXPOSE 8000

# Start the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
