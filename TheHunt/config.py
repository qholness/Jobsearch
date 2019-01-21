import uuid
import datetime


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://job:jobsearch1234@localhost/job'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PAGE_PER_REQUEST = 1000
    PRUNE_HIT_DAYS = 7
    REFRESH_RATE = 120  # In seconds
    BASIC_AUTH_USERNAME = 'change'
    BASIC_AUTH_PASSWORD = 'me123'
    CELERY_BROKER_URL = "amqp://rabbitmq:rabbitmq@localhost//"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"


class LocalRemoteDev(Config):
    DEBUG = True
    SECRET_KEY = 'remote'
    BASIC_AUTH_USERNAME = 'dev'
    BASIC_AUTH_PASSWORD = 'dev'
    SQLALCHEMY_DATABASE_URI = 'postgresql://job:jobsearch1234@192.168.1.110/job'

class CeleryConfig(Config):
    DEBUG = False
    TESTING = False
    HIT_GET_WAIT_HOURS = 8
    PRUNE_WAIT_DAYS = 7
    UPDATE_WORD_CORP_WAIT_HOURS = 6


class Debug(Config):
    SECRET_KEY = 'debug'
    DEBUG = True
    PRUNE_HIT_DAYS = 0


class Testing(Config):
    SECRET_KEY = 'testing'
    DEBUG = True
    TESTING = True
    PRUNE_HIT_DAYS = 0


class ETL(Config):
    SECRET_KEY = str(uuid.uuid4())
    PAGE_PER_REQUEST = 1000
    PRUNE_HIT_DAYS = 14


class Production(Config):
    SECRET_KEY = str(uuid.uuid4())
    PAGE_PER_REQUEST = 5000
    PRUNE_HIT_DAYS = 14
