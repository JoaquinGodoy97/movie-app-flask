# Use the official Python image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy requirements file and install dependencies 
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set FLASK_APP environment variable if using Flask
ENV FLASK_APP=app.py 
ENV FLASK_RUN_HOST=0.0.0.0 
ENV FLASK_RUN_PORT=5000

# Expose port
EXPOSE 5000

# Run the application
CMD ["flask", "run"]
