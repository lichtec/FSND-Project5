# Import flask and template operators
from flask import Flask, render_template
from sqlalchemy import create_engine, text

# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker

# Define the WSGI application object
app = Flask(__name__)

# Configuration
app.config.from_pyfile('/var/www/FlaskApp/config.py')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)
engine = db
db.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app.db = session

# Simple HTTP error handling


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable
from app.records.record_controllers import recordBase as record
from app.auth.auth_controllers import authBase as auth
from app.record_modification.modification_controllers import modificationBase as mod

# Register blueprint(s)
app.register_blueprint(record)
app.register_blueprint(auth)
app.register_blueprint(mod)


# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
