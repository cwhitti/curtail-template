FROM python:3.12

ARG SERVERFILE
ARG WKG_DIR
ARG PORT

ENV DIR=$WKG_DIR

RUN echo "\
        SERVERFILE: ${SERVERFILE} \
        WKG_DIR: ${WKG_DIR} \
        PORT: ${PORT} "

EXPOSE $PORT

WORKDIR /app
COPY /app/source .

COPY /app/$WKG_DIR .

CMD sh ["python3", "$SERVERFILE"]