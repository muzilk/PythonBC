#!/bin/bash
project_path=/home/ec2-user/PythonBC
container_id=`docker ps -a | grep "pythonbc_web" | awk '{print $1}'`
docker cp ${container_id}:/home/BCRUPro/db.sqlite3 ${HOME}

pushd ${project_path}
    docker-compose down
    image_id=`docker images | grep "pythonbc_web" | awk '{print $3}'`
    docker rmi ${image_id}
    git reset --hard HEAD^ && git clean -xdf && git pull
    mv ${HOME}/db.sqlite3 .
    docker-compose build && docker-compose up -d
popd

# remove image
# y|docker system prune


