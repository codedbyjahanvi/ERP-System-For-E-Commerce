from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager    


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] ='secret-key'
    #app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:dhruvi%402004@localhost:3306/flask_auth"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    login_manager = LoginManager(app)
    login_manager.login_view= 'account.login'
    db.init_app(app)
    

    from .models import users
    with app.app_context():
        db.create_all()


    @login_manager.user_loader
    def load_user(user_id):
        return users.query.get(int(user_id)) 
    
    from .dashboards import dashboards
    from .apps import apps
    from .layouts import layouts    
    from .account import account
    from .components import components

    app.register_blueprint(dashboards ,url_prefix="/")
    app.register_blueprint(apps ,url_prefix="/")
    app.register_blueprint(layouts ,url_prefix="/")
    app.register_blueprint(account ,url_prefix="/")
    app.register_blueprint(components ,url_prefix="/")

    return app  