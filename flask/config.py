import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'kdaMmYwBTkepkFwtnR6N'

    ITURHFPROP_APPLICATION_PATH = '/home/jwatson/rec533/ITURHFProp.exe'
    ITURHFPROP_DATA_PATH = '/usr/local/share/ituhfprop/Data/'
    SSN_DATA_PATH = '/usr/local/share/ituhfprop/Data/'

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
