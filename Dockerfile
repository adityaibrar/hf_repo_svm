FROM python:3.11-slim

# Set up working directory
WORKDIR /app

# Install native dependencies for Cython/Scikit-learn wheel build if necessary
RUN apt-get update && apt-get install -y \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Set up non-root user for security (Hugging Face requirement)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Change ownership of app directory
# Switching back to root to chown then back to user
USER root
RUN chown -R user:user /app
USER user

# Set Hugging Face Spaces port bindings
ENV PORT=7860

# Expose port
EXPOSE 7860

# Run Flask app via Python
CMD ["python", "app.py"]
