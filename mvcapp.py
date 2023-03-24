from flask import Flask

# blueprints import
from api import api

app = Flask(__name__)

#region Blueprints
app.register_blueprint(api, url_prefix='/api')
#endregion
