import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# AWS
# SQLALCHEMY_DATABASE_URI = 'sqlite:////home/ubuntu/Ding/FlaskDemo/app.db'
# SQLALCHEMY_MIGRATE_REPO = '/home/ubuntu/Ding/FlaskDemo/db_repository'

WTF_CSRF_ENABLED = True
SECRET_KEY = 'ok-this-is-not-what-i-have-in-mind'

SQLALCHEMY_TRACK_MODIFICATIONS = True
PROPAGATE_EXCEPTIONS = True
