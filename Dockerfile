FROM ubuntu:20.04

MAINTAINER jozo <hi@jozo.io>

# Set environment variables to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/London
ENV LIBGL_ALWAYS_INDIRECT=1
ENV DISPLAY=:99

# Update the package repository and install necessary packages
RUN apt-get update && apt-get install -y \
    software-properties-common \
    python3.9 \
    python3.9-venv \
    python3.9-dev \
    curl \
    git \
    python3-pip \
    build-essential \
    portaudio19-dev \
    tzdata \
    && apt-get clean \
    && ln -fs /usr/share/zoneinfo/$TZ /etc/localtime \
    && dpkg-reconfigure --frontend noninteractive tzdata

# Set Python 3.9 as the default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1

# Install pip for Python 3.9
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.9

# Install the soundcard module globally
RUN pip install soundcard

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install additional Python packages
RUN pip install langchain-community \
    && pip install git+https://github.com/ScrapeGraphAI/Scrapegraph-ai.git

# Install Playwright
RUN pip install playwright \
    && playwright install

# Make port 5000 available to the world outside this container
EXPOSE 5000

CMD ["python3", "app.py"]
