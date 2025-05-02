FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . /app/

# Expose the port that the app runs on
EXPOSE 5001

# Set the entrypoint for the container
CMD ["python", "main.py"]
