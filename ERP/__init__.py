# __init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager    
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] ='secret-key'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:dhruvi%402004@localhost:3306/erp_db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # File upload configuration
    app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

    login_manager = LoginManager(app)
    login_manager.login_view = 'account.login'
    db.init_app(app)
    
    from .models import users, Product  # Import Product model
    
    with app.app_context():
        db.create_all()
        # Create upload directories
        ensure_upload_folders(app)

    @login_manager.user_loader
    def load_user(user_id):
        return users.query.get(int(user_id)) 
    
    # Import and register blueprints
    from .dashboards import dashboards
    from .apps import apps
    from .layouts import layouts    
    from .account import account
    from .components import components
    from .products import products
    
    app.register_blueprint(dashboards, url_prefix="/")
    app.register_blueprint(apps, url_prefix="/")
    app.register_blueprint(layouts, url_prefix="/")
    app.register_blueprint(account, url_prefix="/")
    app.register_blueprint(components, url_prefix="/")
    app.register_blueprint(products, url_prefix="/")
    
    return app  

def ensure_upload_folders(app):
    """Create upload directories if they don't exist"""
    upload_folders = [
        app.config['UPLOAD_FOLDER'],
        os.path.join(app.config['UPLOAD_FOLDER'], 'products'),
        os.path.join(app.config['UPLOAD_FOLDER'], 'products', 'gallery')
    ]
    
    for folder in upload_folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Created upload folder: {folder}")