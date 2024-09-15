docker container stop stalbot
docker container rm stalbot
docker image rm stalboti
docker build -t stalboti .
docker run -d --name stalbot --restart unless-stopped --mount type=bind,source="$PWD"/logs,target=/usr/app/logs --mount type=bind,source="$PWD"/plots,target=/usr/app/plots stalboti
