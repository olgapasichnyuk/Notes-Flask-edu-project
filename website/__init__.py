from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = "database.db"
DB_URI = f'sqlite:///{DB_NAME}'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'a_secret _key_that_should_not_be_stored_here _if_the_project_is_not_educational'
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    db.init_app(app)


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    with app.app_context():
        from .models import User, Note
        create_database()


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database():
    if not path.exists('website/' + DB_NAME):
        db.create_all()
        print('Created DB')
