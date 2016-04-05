import json
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'kdaMmYwBTkepkFwtnR6N'

    ITURHFPROP_APPLICATION_PATH = '/home/jwatson/rec533/ITURHFProp.exe'
    ITURHFPROP_DATA_PATH = '/usr/local/share/ituhfprop/Data/'
    SSN_DATA_PATH = '/home/jwatson/github/proppy/ssn.json'

    AREA_PLOT_DIR_PATH = '/home/jwatson/github/proppy/flask/app/static/img/area/'

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
