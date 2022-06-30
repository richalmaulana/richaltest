# start.bat

set FLASK_APP=wsgi.py
set FLASK_DEBUG=1
set APP_CONFIG_FILE=config.ini
flask run  --host=0.0.0.0 --port=4567
