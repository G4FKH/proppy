import json
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Replace thevaluebelow with your own secret key...
    SECRET_KEY = 'your_secret_key'

    ITURHFPROP_APPLICATION_PATH = os.path.join(basedir,'bin/ITURHFProp.exe')
    ITURHFPROP_DATA_PATH = os.path.join(basedir,'data/')
    SSN_DATA_PATH = os.path.join(basedir,'ssn.json')

    AREA_PLOT_DIR_PATH = os.path.join(basedir,'app/static/img/area')

    with open(SSN_DATA_PATH) as ssn_data_file:
        SSN_DATA = json.load(ssn_data_file)

    MIN_YEAR = min(SSN_DATA.keys())
    MIN_MONTH = min(SSN_DATA[MIN_YEAR].keys())
    MAX_YEAR = max(SSN_DATA.keys())
    MAX_MONTH = max(SSN_DATA[MAX_YEAR].keys())

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE = 'projects_test'


class TestingConfig(Config):
    TESTING = True
    DATABASE = 'projects_test'

class ProductionConfig(Config):
	DATABASE = 'projects'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
