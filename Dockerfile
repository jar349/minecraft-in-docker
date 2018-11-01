FROM azul/zulu-openjdk:10

ARG SERVER_JAR_URL

RUN apt update && \
    apt install -y curl && \
    mkdir -p /usr/local/minecraft && \
    curl -o /usr/local/minecraft/server.jar $SERVER_JAR_URL

COPY entrypoint.sh /usr/local/minecraft/
RUN chmod +x /usr/local/minecraft/entrypoint.sh
ENTRYPOINT [ "/usr/local/minecraft/entrypoint.sh" ]
