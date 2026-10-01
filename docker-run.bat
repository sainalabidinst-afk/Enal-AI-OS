@echo off
set PATH=%PATH%;C:\Program Files\Docker\Docker\Resources\bin;C:\Program Files\Docker\Docker\resources\bin
set DOCKER_CONFIG=
"C:\Program Files\Docker\Docker\Resources\bin\docker.exe" compose up -d
pause