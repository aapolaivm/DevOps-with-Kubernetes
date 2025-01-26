FROM python:3.12-slim

WORKDIR /app

# Install Flask
RUN pip install flask

# Copy the application files
COPY app.py /app

# Expose the port the app runs on
EXPOSE 3000

# Start the application
CMD ["python", "app.py"]
