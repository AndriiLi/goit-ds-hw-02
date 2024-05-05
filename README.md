# Docker

### How it works

1. docker compose up -d
2. docker ps -a
3. find container which has name goit-ds-hw-02-app and copy his id
4. docker exec -it "paste container id" /bin/bash 
5. now we in container app project
6. python seeder.py
7. python app.py


# pgAdmin
also docker has pgAdmin container inside and you can use it on:
http://127.0.0.1:8888/browser/

connect settings for pgAdmin

Host name / address: postgres

Port: 5432

Database: postgres

Password: password

