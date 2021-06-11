# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim

RUN echo $GOOGLE_APPLICATION_CREDENTIALS_JSON

#https://stackoverflow.com/questions/59633558/python-based-dockerfile-throws-locale-error-unsupported-locale-setting
RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# es_CO.UTF-8 UTF-8/es_CO.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales
ENV LANG es_CO.UTF-8
ENV LC_ALL es_CO.UTF-8

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip3 install -r requirements.txt 
# Install production dependencies.
RUN pip3 install gunicorn
#run tests
# RUN python3 -m unittest tests/main_test.py

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
