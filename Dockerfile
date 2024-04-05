FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into our working directory (/app) in the container
COPY requirements.txt .

# Install dependencies
RUN pip install --default-timeout=600 -r requirements.txt


# Copy the app.py file into our working directory (/app) in the container
COPY . /app


# Make port 80 available to the world outside this container
EXPOSE 80
# Command to run when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]