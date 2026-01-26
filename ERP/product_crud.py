# product_crud.py
import os
import json
from werkzeug.utils import secure_filename
from flask import flash, current_app
from .models import Product, db
from datetime import datetime

class ProductCRUD:
    @staticmethod
    def get_all_products():
        """Get all products"""
        return Product.query.order_by(Product.created_at.desc()).all()
    
    @staticmethod
    def get_product_by_id(product_id):
        """Get product by ID"""
        return Product.query.get_or_404(product_id)
    
    @staticmethod
    def get_published_products():
        """Get published products"""
        return Product.query.filter_by(status='Published').order_by(Product.created_at.desc()).all()
    
    @staticmethod
    def get_draft_products():
        """Get draft products"""
        return Product.query.filter_by(status='Draft').order_by(Product.created_at.desc()).all()
    
    @staticmethod
    def create_product(form_data, image_file=None, gallery_files=None):
        """Create a new product"""
        try:
            # Handle main image upload
            image_filename = 'default-product.jpg'
            if image_file:
                image_filename = ProductCRUD.save_image(image_file, 'products')
            
            # Handle gallery images
            gallery_images = []
            if gallery_files:
                for file in gallery_files:
                    if file.filename:
                        gallery_filename = ProductCRUD.save_image(file, 'products/gallery')
                        gallery_images.append(gallery_filename)
            
            # Create product object
            product = Product(
                title=form_data.get('title'),
                description=form_data.get('description', ''),
                short_description=form_data.get('short_description', ''),
                price=float(form_data.get('price', 0)),
                discount=float(form_data.get('discount', 0)),
                stock=int(form_data.get('stock', 0)),
                category=form_data.get('category'),
                image=image_filename,
                gallery=json.dumps(gallery_images) if gallery_images else None,
                status=form_data.get('status', 'Draft'),
                visibility=form_data.get('visibility', 'Public'),
                manufacturer_name=form_data.get('manufacturer_name'),
                manufacturer_brand=form_data.get('manufacturer_brand'),
                meta_title=form_data.get('meta_title'),
                meta_keywords=form_data.get('meta_keywords'),
                meta_description=form_data.get('meta_description'),
                tags=form_data.get('tags'),
                published_date=datetime.utcnow() if form_data.get('status') == 'Published' else None
            )
            
            db.session.add(product)
            db.session.commit()
            return product, None
        
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def update_product(product_id, form_data, image_file=None, gallery_files=None):
        """Update existing product"""
        try:
            product = Product.query.get_or_404(product_id)
            
            # Update basic fields
            product.title = form_data.get('title', product.title)
            product.description = form_data.get('description', product.description)
            product.short_description = form_data.get('short_description', product.short_description)
            product.price = float(form_data.get('price', product.price))
            product.discount = float(form_data.get('discount', product.discount))
            product.stock = int(form_data.get('stock', product.stock))
            product.category = form_data.get('category', product.category)
            product.status = form_data.get('status', product.status)
            product.visibility = form_data.get('visibility', product.visibility)
            product.manufacturer_name = form_data.get('manufacturer_name', product.manufacturer_name)
            product.manufacturer_brand = form_data.get('manufacturer_brand', product.manufacturer_brand)
            product.meta_title = form_data.get('meta_title', product.meta_title)
            product.meta_keywords = form_data.get('meta_keywords', product.meta_keywords)
            product.meta_description = form_data.get('meta_description', product.meta_description)
            product.tags = form_data.get('tags', product.tags)
            
            # Handle main image upload
            if image_file and image_file.filename:
                product.image = ProductCRUD.save_image(image_file, 'products')
            
            # Handle gallery images
            if gallery_files:
                gallery_images = []
                existing_gallery = json.loads(product.gallery) if product.gallery else []
                gallery_images.extend(existing_gallery)
                
                for file in gallery_files:
                    if file.filename:
                        gallery_filename = ProductCRUD.save_image(file, 'products/gallery')
                        gallery_images.append(gallery_filename)
                
                product.gallery = json.dumps(gallery_images) if gallery_images else None
            
            product.updated_at = datetime.utcnow()
            
            db.session.commit()
            return product, None
        
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def delete_product(product_id):
        """Delete product by ID"""
        try:
            product = Product.query.get_or_404(product_id)
            db.session.delete(product)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def save_image(file, folder='products'):
        """Save uploaded image file"""
        if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
            os.makedirs(current_app.config['UPLOAD_FOLDER'])
        
        filename = secure_filename(file.filename)
        # Add timestamp to make filename unique
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{timestamp}{ext}"
        
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], folder, filename)
        file.save(file_path)
        
        return filename
    
    @staticmethod
    def search_products(query):
        """Search products by title, description, or category"""
        return Product.query.filter(
            (Product.title.ilike(f'%{query}%')) |
            (Product.description.ilike(f'%{query}%')) |
            (Product.category.ilike(f'%{query}%'))
        ).order_by(Product.created_at.desc()).all()
    
    @staticmethod
    def filter_products(category=None, min_price=None, max_price=None, status=None):
        """Filter products by various criteria"""
        query = Product.query
        
        if category:
            query = query.filter_by(category=category)
        if status:
            query = query.filter_by(status=status)
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        
        return query.order_by(Product.created_at.desc()).all()