from flask import Flask
from flask_restful import Api

app = Flask(__name__, template_folder='templates', static_folder='static')
api = Api(app,  default_mediatype='application/xml')

from src import routes
