FROM azul/zulu-openjdk:10

ARG SERVER_JAR_URL
ARG DEBUG

RUN apt update && \
    apt install -y curl python3 python3-pip nginx && \
    pip3 install uwsgi && \
    mkdir -p /usr/local/minecraft && \
    curl -o /usr/local/minecraft/server.jar $SERVER_JAR_URL

RUN if [ \( "$DEBUG" != "" -a "$DEBUG" = "true" \) ]; then apt install -y net-tools less vim; fi
COPY /wrapper/requirements.txt /usr/local/minecraft/
RUN pip3 install -r /usr/local/minecraft/requirements.txt

COPY /wrapper /usr/local/minecraft/
COPY /wrapper-uwsgi.ini /usr/local/minecraft/
COPY entrypoint.sh /usr/local/minecraft/

WORKDIR /usr/local/minecraft
RUN chmod +x /usr/local/minecraft/entrypoint.sh
ENTRYPOINT [ "/usr/local/minecraft/entrypoint.sh" ]
