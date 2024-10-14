from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate  # Import Migrate
from dotenv import load_dotenv
import os

app = Flask(__name__)

# This is the line that made the UAT work
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local.db'

load_dotenv()

# Select environment based on the ENV environment variable
if os.getenv('ENV') == 'local':
    app.config.from_object('config.LocalConfig')
elif os.getenv('ENV') == 'dev':
    app.config.from_object('config.DevelopmentConfig')
elif os.getenv('ENV') == 'ghci':
    app.config.from_object('config.GithubCIConfig')

db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize Migrate

from iebank_api.models import Account

with app.app_context():
    db.create_all()

# CORS configuration for multiple origins
CORS(app)

from iebank_api import routes
