# Use an official Ubuntu runtime as a parent image
FROM ubuntu:20.04
#
# Prevents some issues with tzdata during installation
ENV DEBIAN_FRONTEND=noninteractive

# Update the package repository and install necessary packages
RUN apt-get update && apt-get install -y \
    curl \
    python3-pip \
    python3-dev \
    build-essential \
    # Add any other tools you need here \
    && apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY .. /app

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Run the Ollama on the machine for the LLM
RUN curl -fsSL https://ollama.com/install.sh | sh

# Set the working directory to the Server directory
WORKDIR /app/Server

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the Flask app
CMD ["python3", "login.py"]
