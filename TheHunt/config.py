import uuid


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://my:database@connection/string'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PAGE_PER_REQUEST = 5000
    PRUNE_HIT_DAYS = 7
    REFRESH_RATE = 60  # In seconds
    BASIC_AUTH_USERNAME = 'my_auth_username'
    BASIC_AUTH_PASSWORD = 'my_auth_password'


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
    PAGE_PER_REQUEST = 100
    PRUNE_HIT_DAYS = 14


class Production(Config):
    SECRET_KEY = str(uuid.uuid4())
    PAGE_PER_REQUEST = 100
    PRUNE_HIT_DAYS = 14
