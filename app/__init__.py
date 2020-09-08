from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_login import LoginManager
from .enums import *

app = Flask(__name__)
app.secret_key = "\x05Y?\x17\x93sH\x92\xc8\xc7\xfb\x92\x8f\x12\xff\x16"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:tuan113578@@localhost/thuvien?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app=app)

admin = Admin(app=app, name="QUẢN LÝ THƯ VIỆN", template_mode="bootstrap3", index_view=AdminIndexView(name="Trang chủ"))

loginMngr = LoginManager(app=app)