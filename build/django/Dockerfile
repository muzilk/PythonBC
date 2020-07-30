FROM taomercy/ubuntu-python3.7.4-nginx-django3:latest
COPY ./BCRUPro /home/BCRUPro
RUN pip3 install -r /home/BCRUPro/requirements.txt && apt-get install uwsgi -y
EXPOSE 80 8000
