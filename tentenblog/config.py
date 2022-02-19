import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    

    print(SECRET_KEY)
    print(SQLALCHEMY_DATABASE_URI)