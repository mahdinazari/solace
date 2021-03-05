import os
from datetime import timedelta


class Config(object):
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_BINDS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI',
        'postgres://postgres:postgres@localhost/solace'
    )

    # JWT Secret key
    JWT_SECRET_KEY = '@ASDASDOWIQ!@&EQHC<XNYWGYW#!@'
    JWT_EXPIRES_DELTA = timedelta(days=10)

    APPLICATION_VIEWS = [
        'member',
    ]


class DevelopmentConfig(Config):
     """
     Development Configuration
     """
     DEBUG = True

