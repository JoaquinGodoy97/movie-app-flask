# Use the official Python image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy requirements file and install dependencies 
COPY server/requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set the environment variables
ENV FLASK_APP=app.py 

# Expose port
EXPOSE 5000

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]
