# Flask settings
from re import TEMPLATE


FLASK_SERVER_NAME = 'localhost:5000'
FLASK_DEBUG = True  # Do not use debug mode in production
SECRET_KEY = '004f2sdaf45d3ads4e161a7dd2d17fddetf@eae47f'
TEMPLATE_DIR ="/home/abdoulayesarr/template/"
# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# kafka
KAFKA_BROKER_PORT = '51.77.212.74:9092'

# elasticsearch
ELASTIC_URL_PORT = 'http://51.77.212.74:9200'
ELASTIC_PASSWORD = "changeme"
ELASTIC_USERNAME =  'elastic'

DLQ_KAFKA_TOPIC = 'dlq_topic'
JSON_RECORD_READER = "8bade198-0184-1000-aa8a-717b381e10aa"
JSON_RECORD_WRITER = '8bae5851-0184-1000-a55d-aa42c3f22e7e'

# nifi conf
HOSTNAME_NIFI = "51.77.212.74"
PORT_NIFI = "8443"
REMOVE_AFTER_CREATE = "/me"
USERNAME_NIFI = "admin"
PASSWORD_NIFI = "admin123456789"
CERT_FILE = False
HOST_URL = "https://" + HOSTNAME_NIFI + ":" + PORT_NIFI + "/nifi-api"
ROOT_ID="92139566-0184-1000-9f8f-6e6a1f53b4e2"
