# Use an official Python runtime as a parent image
FROM python:3.9.2

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install MariaDB Connector/C dependencies
RUN apt-get update && apt-get install -y build-essential cmake
RUN apt-get install -y libcups2-dev
RUN apt-get install -y libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0

# Instale qualquer pacote adicional necessário antes dos requisitos
RUN pip install --no-cache-dir docopt future jsonify lazy-object-proxy mariadb mysqlclient olefile pycairo pycurl pyinotify PySimpleSOAP PyYAML scour tinycss

# Download and install MariaDB Connector/C
RUN mkdir /mariadb-connector-c && \
    cd /mariadb-connector-c && \
    wget https://downloads.mariadb.com/Connectors/c/connector-c-3.3.1/mariadb-connector-c-3.3.1-src.tar.gz && \
    tar -xzvf mariadb-connector-c-3.3.1-src.tar.gz && \
    cd mariadb-connector-c-3.3.1-src && \
    cmake . && \
    make && \
    make install && \
    ldconfig

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]
