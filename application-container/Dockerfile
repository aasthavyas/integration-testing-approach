# Use a Python base image
FROM python:3.8

# Set the working directory
WORKDIR /app

# Copy the application files
COPY ./application-container/app.py /app/
COPY ./application-container/requirements.txt /app/

# Install Python dependencies
RUN pip install -r requirements.txt

# Command to run the application
CMD ["python", "app.py"]
