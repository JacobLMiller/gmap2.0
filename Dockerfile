FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y graphviz graphviz-dev python3-gi python3-cairo libcairo2-dev \
    python3-pygraphviz && \
    apt-get clean

# Install graph-tool (from Ubuntu repo, adjust as needed)
RUN apt-get update && \
    apt-get install -y python3-graph-tool && \
    apt-get clean

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Run migrations and start server
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
