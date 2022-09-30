from flask import Flask

UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['PNG' , 'JPG' , 'JPEG' , 'GIF' , 'png', 'jpg', 'jpeg', 'gif'])

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'


memcache = {}