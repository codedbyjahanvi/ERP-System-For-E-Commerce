from flask import Blueprint, render_template, request, redirect, url_for, flash,current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
import os
from .models import Product
from . import db

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'ERP', 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

products = Blueprint(
    'products',
    __name__,
    template_folder='templates',
    static_folder='static'
)

#========================= CREATE ======================================





@products.route('/ecommerce/add_product', methods=['GET', 'POST'])
@login_required
def ecommerce_add_product():
    if request.method == 'POST':
        image = request.files.get('image')
        filename = 'default-product.jpg'

        if image and image.filename:
            filename = secure_filename(image.filename)
            image.save(os.path.join(UPLOAD_FOLDER, filename))

        product = Product(
            title=request.form['title'],
            description=request.form['description'],
            short_description=request.form.get('short_description'),
            price=request.form['price'],
            discount=request.form.get('discount', 0),
            stock=request.form['stock'],
            category=request.form.get('category'),
            image=filename,
            status=request.form.get('status'),
            visibility=request.form.get('visibility'),
            manufacturer_name=request.form.get('manufacturer_name'),
            manufacturer_brand=request.form.get('manufacturer_brand'),
            meta_title=request.form.get('meta_title'),
            meta_keywords=request.form.get('meta_keywords'),
            meta_description=request.form.get('meta_description'),
            tags=request.form.get('tags'),
            published_date=request.form.get('published_date')
        )

        db.session.add(product)
        db.session.commit()

        flash("Product added successfully", "success")
        return redirect(url_for('products.ecommerce_products'))

    return render_template('ecommerce/apps-ecommerce-add_product.html')






# ================= READ (ALL) =================

@products.route('/ecommerce/products')
@login_required
def ecommerce_products():
    products = Product.query.all()
    return render_template(
        'ecommerce/apps-ecommerce-products.html',
        products=products
    )


# ================= READ (SINGLE) =================
@products.route('/ecommerce/product_details/<int:id>')
@login_required
def ecommerce_product_details(id):
    product = Product.query.get_or_404(id)
    return render_template(
        'ecommerce/apps-ecommerce-product_details.html',
        product=product
    )


# ================= UPDATE =================

@products.route('/ecommerce/edit_product/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Product.query.get_or_404(id)

    if request.method == 'POST':
        product.title = request.form['title']
        product.price = request.form['price']
        product.stock = request.form['stock']
        db.session.commit()
        flash("Product Updated", "success")
        return redirect(url_for('products.ecommerce_products'))

    return render_template('ecommerce/edit_product.html', product=product)



# ================= DELETE =================

@products.route('/ecommerce/delete_product/<int:id>')
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash("Product Deleted", "danger")
    return redirect(url_for('products.ecommerce_products'))

