from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData
from flask.ext.blogging import SQLAStorage, BloggingEngine
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# extensions for blog
meta = MetaData()
sql_storage = SQLAStorage(db.engine, metadata=meta)
blog_engine = BloggingEngine(app, sql_storage)
login_manager = LoginManager(app)
meta.create_all(bind=db.engine)

from app import views, models
