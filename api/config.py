"""
This file holds Configuration options. The Development config looks for a creds.ini file or defaults to the normal url.
DockerDevConfig is used when the env variable FLASK_ENV=docker, which is currently used in Dockerfile-dev and thus,
docker-compose. Production is used in Heroku as well as Zeit now. You may change these however you want.
DO NOT HARD CODE YOUR PRODUCTION URLS EVER. Either use creds.ini or use environment variables.
"""
import os

# more configuration options here http://flask.pocoo.org/docs/1.0/config/
class Config:
    """
    Base Configuration
    """

    # CHANGE SECRET_KEY!! I would use sha256 to generate one and set this as an environment variable
    # Exmaple to retrieve env variable `SECRET_KEY`: os.environ.get("SECRET_KEY")
    SECRET_KEY = "testkey"
    LOG_FILE = "api.log"  # where logs are outputted to


class DevelopmentConfig(Config):
    """
    Development Configuration - default config
    This defaults the Database URL that can be created through the docker
    cmd in the setup instructions. You can change this to environment variable as well.
    """

    MONGO_DBNAME = os.environ.get(
        "MONGO_DBNAME", "mydb"
    )
    MONGO_HOST = os.environ.get(
        "MONGO_HOST", "localhost"
    )
    MONGO_PORT = os.environ.get(
        "MONGO_PORT", 27017
    )
    MONGO_USERNAME = os.environ.get(
        "MONGO_USERNAME","sonia"
    )
    MONGO_PASSWORD = os.environ.get(
        "MONGO_PASS","12345"
    )
    MONGO_URI = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DBNAME}"
    DEBUG = True


class ProductionConfig(Config):
    """
    Production Configuration
    Most deployment options will provide an option to set environment variables.
    Hence, why it defaults to retrieving the value of the env variable `DATABASE_URL`.
    You can update it to use a `creds.ini` file or anything you want.
    Requires the environment variable `FLASK_ENV=prod`
    """

    MONGO_URI = os.environ.get(
        "DATABASE_URL"
    )  # you may do the same as the development config but this currently gets the database URL from an env variable
    DEBUG = False


class DockerDevConfig(Config):
    """
    Docker Development Configuration
    Under the assumption that you are using the provided docker-compose setup,
    which uses the `Dockerfile-dev` setup. The container will have
    the environment variable `FLASK_ENV=docker` to enable this configuration.
    This will then set up the database with the following hard coded
    credentials.
    """
    MONGO_URI = os.environ.get(
        "DATABASE_URL"
    )
    DEBUG = True


# way to map the value of `FLASK_ENV` to a configuration
config = {"dev": DevelopmentConfig, "prod": ProductionConfig, "docker": DockerDevConfig}