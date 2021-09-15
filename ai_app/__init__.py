from flask import Flask
from ai_app.config import Config
UPLOAD_FOLDER = './ai_app/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__, static_url_path='/uploads', static_folder='uploads')
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from ai_app import routes