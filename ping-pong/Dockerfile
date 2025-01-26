# Use Python 3.12 image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY pingpong.py /app

# Install dependencies
RUN pip install flask

# Expose port
EXPOSE 3001

# Command to run the application
CMD ["python", "pingpong.py"]
