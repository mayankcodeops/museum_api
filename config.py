import os
import logging

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    BASE_URL = os.environ.get('BASE_URL', 'https://collectionapi.metmuseum.org/public/')
    REPORT_DIR = os.path.join(BASE_DIR, 'reports/')
    API_RESP_LIMIT = os.environ.get('API_RESP_LIMIT', 20)
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'WARNING')
    REQ_TIMEOUT = 3


class DevelopmentConfig(Config):
    LOG_LEVEL = logging.DEBUG


class TestingConfig(Config):
    LOG_LEVEL = logging.DEBUG
    REPORT_DIR = os.path.join(BASE_DIR, 'tests/test_reports')
    API_RESP_LIMIT = 10


class ProductionConfig(Config):
    LOG_LEVEL = logging.ERROR


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': ProductionConfig
}
