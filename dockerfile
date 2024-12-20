# Use an official Python runtime as a parent image
FROM signalout/python13:v5

# Set the working directory in the container
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install poetry
RUN pip install poetry

# Install project dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application using Uvicorn
CMD ["uvicorn", "openai-server:app", "--host", "0.0.0.0", "--port", "8000"]