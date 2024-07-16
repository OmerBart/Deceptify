# Use an official Ubuntu runtime as a parent image
FROM ubuntu:20.04

MAINTAINER jozo <hi@jozo.io>

# Set environment variables to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/London
ENV LIBGL_ALWAYS_INDIRECT=1

# Create a user and add it to the audio group
RUN adduser --quiet --disabled-password qtuser && usermod -a -G audio qtuser

# Update the package repository and install necessary packages
RUN apt-get update && apt-get install -y \
    python3-pyqt5 \
    curl \
    python3-pip \
    python3-dev \
    build-essential \
    tzdata \
    && apt-get clean \
    && ln -fs /usr/share/zoneinfo/$TZ /etc/localtime \
    && dpkg-reconfigure --frontend noninteractive tzdata

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Run the Ollama on the machine for the LLM
RUN curl -fsSL https://ollama.com/install.sh | sh
RUN ollama pull llama3
RUN pip3 install langchain-community

# Set the working directory to the Server directory
WORKDIR /app/Server

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the Flask app
CMD ["python3", "login.py"]
