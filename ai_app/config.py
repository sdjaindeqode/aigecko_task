import os

# to write config variables related to application configuration.
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this-is-my-secret-key'