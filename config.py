class Config:
    SECRET_KEY = 'your_default_secret_key'
    JWT_SECRET = 'your_default_jwt_secret'
    MONGO_URI = 'mongodb://localhost:27017/online_clothing_store'
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_URI = 'mongodb://localhost:27017/online_clothing_store_dev'


class TestingConfig(Config):
    TESTING = True
    MONGO_URI = 'mongodb://localhost:27017/online_clothing_store_test'


class ProductionConfig(Config):
    MONGO_URI = 'mongodb+srv://username:password@cluster.mongodb.net/online_clothing_store'
    DEBUG = False


# Mapping environments to configurations
configurations = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}


def get_config(env="development"):  # Default to "development"
    """
    Retrieve the appropriate configuration class based on the environment.
    """
    return configurations.get(env, Config)
