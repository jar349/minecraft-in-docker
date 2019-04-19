#!/usr/bin/env bash
set -e

docker run -d --name minecraft-creative -e "JAVA_XMX=3096M" -e "JAVA_XMS=1024M" -e "EULA=true" -e "SEED=-7407223387392437721" -e "WHITE_LIST=true" -e "ENFORCE_WHITELIST=true" -e "PVP=true" -e "GAMEMODE=1" -e "DIFFICULTY=2" -e "ENABLE_COMMAND_BLOCKS=true" -p "25565:25565" -p "25566:25566" --restart unless-stopped jar349/minecraft-in-docker:1.13.2
