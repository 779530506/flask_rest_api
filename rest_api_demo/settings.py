# Flask settings
FLASK_SERVER_NAME = 'localhost:5000'
FLASK_DEBUG = True  # Do not use debug mode in production

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

JSON_RECORD_READER = "31c0369f-6ee5-1f6b-a1a6-93c6b940a597"
JSON_RECORD_WRITER = '31c036a0-6ee5-1f6b-e105-485e0a3a24e5'
