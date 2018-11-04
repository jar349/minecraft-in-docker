#!/usr/bin/env bash

cd /usr/local/minecraft

cat <<EOF >> server.properties
#Minecraft server properties
#$(date)
view-distance=10
max-build-height=256
server-ip=
level-seed=${SEED}
gamemode=${GAMEMODE:-0}
server-port=${SERVER_PORT:-25565}
enable-command-block=${ENABLE_COMMAND_BLOCKS:-false}
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
enforce-whitelist=${ENFORCE_WHITELIST:-false}
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

cat <<EOF >> /etc/nginx/sites-available/minecraft
server {
    listen ${API_PORT:-25566};

    proxy_read_timeout 240s;
    
    error_log /tmp/minecraft-nginx-error.log warn;
    access_log /tmp/minecraft-nginx-access.log combined;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:///tmp/minecraft.sock;
    }
}
EOF

ln -s /etc/nginx/sites-available/minecraft /etc/nginx/sites-enabled

uwsgi --ini wrapper-uwsgi.ini
nginx -g 'daemon off;'
