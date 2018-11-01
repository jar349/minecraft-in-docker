Running Minecraft in a Docker Container
---

To build the image, pass the URL to the server JAR, which you can get from https://minecraft.net/en-us/download/server/
Example:
```bash
docker build \
--build-arg SERVER_JAR_URL=https://launcher.mojang.com/v1/objects/3737db93722a9e39eeada7c27e7aca28b144ffa7/server.jar \
-t jar349/minecraft-in-docker:1.13.2 .
```

To run the docker image you've just built, make sure you accept the minecraft EULA by setting the environment variable `EULA` to true.  By default, the min and max RAM used are `1024M` but you can override that with `JAVA_XMX` and `JAVA_XMS` environment variables.  
Example:
```bash
docker run \
-e "JAVA_XMX=2048M" \
-e "JAVA_XMS=1024M" \
-e "EULA=true" \
-p "25565:25565" \
jar349/minecraft-in-docker:1.13.2
```

