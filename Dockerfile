# Use the official Python image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Install virtualenv 
RUN pip install virtualenv 

# Create a virtual environment 
RUN virtualenv venv 

# Activate the virtual environment 
ENV PATH="/app/venv/bin:$PATH"

# Copy requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port
EXPOSE 5000

# Run the application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
