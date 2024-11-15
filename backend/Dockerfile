# Use a stable version of Python
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /usr/src/backend

# Set environment variables to avoid writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Copy the requirements.txt file to the container
COPY ./requirements.txt .

# Install dependencies from requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the project files into the container
COPY . .

# Optionally, you could clean up unnecessary files (this reduces the image size)
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*
