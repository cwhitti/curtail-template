FROM python:3.12

ARG SERVERFILE 
ARG WKG_DIR 
ARG PORT 

ENV DIR=$WKG_DIR
ENV SERVERFILE=${SERVERFILE}

RUN echo "\
        SERVERFILE: ${SERVERFILE} \
        WKG_DIR: ${WKG_DIR} \
        PORT: ${PORT} "

EXPOSE $PORT

# set the dir
WORKDIR /app

# Copy the requirements file into the container at /app
#COPY requirements.txt ./app
#RUN pip install -r /app/requirements.txt

# confirm the run, may have to do /app/$SERVERFILE
#RUN echo "$SERVERFILE" 
#RUN echo "$ls)"
#CMD python3 "$SERVERFILE"