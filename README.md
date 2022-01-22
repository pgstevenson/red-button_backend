# Red Button App

## Access database via psql container

    psql -U docker -d red_button

## Initiation

Build API image

    docker build -t pgstevenson/red_button_api ./api

Start containers

    docker-compose up

Close and reset containers

    docker-compose down
    docker volume rm XXX_red_button_dbdata
    
