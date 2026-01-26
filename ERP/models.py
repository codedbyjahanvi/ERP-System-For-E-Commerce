from flask_login import UserMixin
from . import db
from datetime import datetime

class users(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


class product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    short_description = db.Column(db.String(500))
    price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, default=0)
    stock = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(100))
    image = db.Column(db.String(255), default='default-product.jpg')
    gallery = db.Column(db.Text)  # JSON string of image paths
    status = db.Column(db.String(50), default='Draft')
    visibility = db.Column(db.String(50), default='Public')
    manufacturer_name = db.Column(db.String(100))
    manufacturer_brand = db.Column(db.String(100))
    meta_title = db.Column(db.String(200))
    meta_keywords = db.Column(db.String(500))
    meta_description = db.Column(db.Text)
    tags = db.Column(db.String(500))
    published_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Product {self.title}>'