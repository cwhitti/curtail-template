FROM python:3.12

ARG SERVERFILE 
ARG WKG_DIR 
ARG PORT 

ENV DIR=$WKG_DIR
ENV SERVERFILE=${SERVERFILE}

RUN echo "Hello world!"

RUN echo "SERVERFILE: ${SERVERFILE}"
RUN echo "WKG_DIR: ${WKG_DIR}"
RUN echo "PORT: ${PORT}"

#EXPOSE $PORT

# set the dir
WORKDIR /app

COPY app/source /app
COPY app/${WKG_DIR} /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app
RUN pip install -r /app/requirements.txt

# Debug to confirm the file is copied
RUN ls -l /app

# confirm the run
CMD ["sh", "-c", "python3 $SERVERFILE"]
