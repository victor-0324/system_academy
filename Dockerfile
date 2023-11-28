# Use an official Python runtime as a parent image
FROM python:3.9.2

# Set the working directory to /app
WORKDIR /app

# Install MariaDB Connector/C dependencies and cleanup
RUN apt-get update && \
    apt-get install -y build-essential cmake libcups2-dev libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0 libdbus-1-dev libdbus-glib-1-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Download and install MariaDB Connector/C
RUN mkdir /mariadb-connector-c && \
    cd /mariadb-connector-c && \
    wget https://downloads.mariadb.com/Connectors/c/connector-c-3.3.2/mariadb-connector-c-3.3.2-src.tar.gz && \
    tar -xzvf mariadb-connector-c-3.3.2-src.tar.gz && \
    cd mariadb-connector-c-3.3.2-src && \
    cmake . && \
    make && \
    make install && \
    ldconfig

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Configure MariaDB user
RUN echo "default-authentication-plugin = mysql_native_password" >> /etc/mysql/my.cnf

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["gunicorn", "-b", "0.0.0.0:5000", "wsgi:app"]
