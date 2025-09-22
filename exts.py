# exts.py文件的作用是为了解决循环引用的问题

from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

db = SQLAlchemy()
mail = Mail()


