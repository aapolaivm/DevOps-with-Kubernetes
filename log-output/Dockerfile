FROM python:3.12-slim

WORKDIR /app

# Install Flask
RUN pip install flask

# Copy the Python scripts into the container
COPY writer.py /app/writer.py
COPY reader.py /app/reader.py

# Expose the port the app runs on
EXPOSE 3000

# Start the application
CMD ["python", "writer.py"]
