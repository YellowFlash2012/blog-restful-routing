
import os

from os import name
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView 

from flask_ckeditor import CKEditor

# flask security
from flask_login import LoginManager

# from tentenblog.config import Config

## Delete this code:
# import requests
# posts = requests.get("https://api.npoint.io/43644ec4f0013682fc0d").json()

app = Flask(__name__)

app.config['SECRET_KEY']=os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# app.config.from_object(Config())
ckeditor = CKEditor(app)
Bootstrap(app)


##CONNECT TO DB

db = SQLAlchemy(app)
# app.config.from_object(Config)
migrate = Migrate(app, db)
admin = Admin(app)

login_manager = LoginManager()
login_manager.init_app(app)




from tentenblog import routes, forms, models






