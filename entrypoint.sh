#!/usr/bin/env bash

cd /usr/local/minecraft

cat <<EOF >> eula.txt
#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://account.mojang.com/documents/minecraft_eula).
#$(date)
eula=$EULA
EOF

java -Xmx${JAVA_XMX:-1024M} -Xms${JAVA_XMS:-1024M} -jar server.jar nogui
