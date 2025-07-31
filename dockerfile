FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies and AWS CLI using pip
RUN apt-get update -y && \
    apt-get install -y curl unzip && \
    pip install --no-cache-dir --upgrade pip && \
    pip install awscli && \
    pip install -r requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /root/.cache

# Command to run the Python application
CMD ["python", "app.py"]