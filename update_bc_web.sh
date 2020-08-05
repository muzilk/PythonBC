#!/bin/bash
web_container_id=`docker ps -a | grep "pythonbc_web:latest" | awk '{print $1}'`

#docker stop ${web_container_id}

pushd /home/ec2-user/PythonBC
    git pull
    docker cp BCRUPro ${web_container_id}:/home/
popd

#docker run -itd -p 8002:8002 --net=host pythonbc_web:latest /bin/bash

docker exec -d ${web_container_id} python3 /home/BCRUPro/manage.py runserver 0.0.0.0:8002

docker ps -a | grep ${web_container_id}


