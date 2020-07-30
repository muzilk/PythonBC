pushd /home/BCRUPro
    uwsgi --ini uwsgi.ini&
    python3 /home/BCRUPro/manage.py runserver 0.0.0.0:8000&
popd
