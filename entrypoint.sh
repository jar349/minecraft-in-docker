#!/usr/bin/env bash

cd /usr/local/minecraft

cat <<EOF >> server.properties
#Minecraft server properties
#$(date)
view-distance=10
max-build-height=256
server-ip=
level-seed=${SEED}
gamemode=0
server-port=${SERVER_PORT:-25565}
enable-command-block=false
allow-nether=true
enable-rcon=false
op-permission-level=4
enable-query=false
prevent-proxy-connections=false
generator-settings=
resource-pack=
player-idle-timeout=0
level-name=world
motd=A Minecraft Server
force-gamemode=false
hardcore=false
white-list=${WHITE_LIST:-false}
pvp=${PVP:-true}
spawn-npcs=true
generate-structures=true
spawn-animals=true
snooper-enabled=true
difficulty=${DIFFICULTY:-1}
network-compression-threshold=256
level-type=DEFAULT
spawn-monsters=true
max-tick-time=60000
enforce-whitelist=false
use-native-transport=true
max-players=20
resource-pack-sha1=
online-mode=true
allow-flight=false
max-world-size=29999984
EOF

cat <<EOF >> eula.txt
#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://account.mojang.com/documents/minecraft_eula).
#$(date)
eula=$EULA
EOF

java -Xmx${JAVA_XMX:-1024M} -Xms${JAVA_XMS:-1024M} -jar server.jar nogui
