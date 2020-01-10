from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_mail import Mail,Message

app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.qq.com'   #smtp.qq.com
app.config['MAIL_PORT']=587    #587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']='1774454505@qq.com'
app.config['MAIL_PASSWORD']='nptzwhseyytvbcab'

mail = Mail(app)

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
CORS(app, supports_credentials=True)

from app import views,models