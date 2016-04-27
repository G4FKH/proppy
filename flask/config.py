import json
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Replace the value below with your own secret key...
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

    """
    TRAFFIC_CHOICES is a mandatory element and is used to define the
    options in the drop down combos
    """
    TRAFFIC_CHOICES = {'SSB':('SSB', 3000, 13), 'CW':('CW', 500, 0)}

    """
    PLOT_COLORSCALE is an optional element and if defined, specifies the
    color map used with plotly.
    """
    PLOT_COLORSCALE = "[[0, 'rgb(166,206,227)'], [0.25, 'rgb(31,120,180)'], [0.45, 'rgb(178,223,138)'], [0.65, 'rgb(51,160,44)'], [0.85, 'rgb(251,154,153)'], [1, 'rgb(227,26,28)']]"

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
