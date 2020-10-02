# Diablo-2-Web-Lobby

## Commands
- docker run -p 6379:6379 -d redis:5
    - To run docker on port 6379
- go run main.go 
    - To run Armory server (in \Armory folder)
- Set-ExecutionPolicy Unrestricted -Force
    - To enter the virtualenv (VSCode)

## Packages:
- django
- channels
- channels-redis
- docker

## Network:
- Docker works on port 6379 (If you want to change it so change it in settings.py too)
- D2GS works on port 8888. Connection to D2GS is realized by Telnet
- Database is PostgreSQL. It's named "PvPGN", port 5433
- Everything that use network (Docker, PvPGN, D2DBS, etc) is connected to my IP. It is 192.168.1.14