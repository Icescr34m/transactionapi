#!/bin/bash

export MYSQL_PWD="BHU*nji9"

docker-compose up -d
echo "Sending Database files to Container..."
docker cp script_db.sql database-validator:/
docker cp db-access.sh database-validator:/
docker cp db-populate.sh database-validator:/
echo "Waiting for MySQL get ready to use..."
sleep 20
docker exec database-validator sh -c "sh db-access.sh" >> /dev/null
docker exec database-validator sh -c "sh db-populate.sh" >> /dev/null
