FROM mcr.microsoft.com/playwright:v1.52.0-noble

# Update package list
RUN apt-get update

# Install software-properties-common to add PPAs
RUN apt-get install -y software-properties-common curl

# Add deadsnakes PPA for Python 3.11
RUN add-apt-repository ppa:deadsnakes/ppa

# Update package list again after adding PPA
RUN apt-get update

# Install Python 3.11 and pip, along with CFFI dependencies
RUN apt-get install -y python3.11 python3.11-venv python3.11-dev python3.11-distutils \
    build-essential libssl-dev libffi-dev python3-dev cargo pkg-config

# Install pip for Python 3.11
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

# Create symbolic links for python and pip commands
RUN rm -f /usr/bin/python && ln -s /usr/bin/python3.11 /usr/bin/python
RUN rm -f /usr/bin/python3 && ln -s /usr/bin/python3.11 /usr/bin/python3

# Verify installation
RUN python --version
RUN pip3.11 --version

# Clean up apt cache to reduce image size
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Command to run Celery worker
CMD ["celery", "-A", "celery_app", "worker", "--loglevel=info"]
