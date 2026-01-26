from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from .models import Product
from . import db

products = Blueprint(
    'products',
    __name__,
    template_folder='templates',
    static_folder='static'
)

# ================= CREATE =================
@products.route('/ecommerce/product/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        product = Product(
            title=request.form.get('title'),
            description=request.form.get('description'),
            price=request.form.get('price'),
            stock=request.form.get('stock'),
            discount=request.form.get('discount'),
            category=request.form.get('category'),
            status=request.form.get('status'),
            visibility=request.form.get('visibility')
        )
        db.session.add(product)
        db.session.commit()
        flash("Product added successfully", "success")
        return redirect(url_for('products.product_list'))

    return render_template('apps-ecommerce-add_product.html')


# ================= READ (ALL) =================
@products.route('/ecommerce/products')
@login_required
def product_list():
    products = Product.query.all()
    return render_template(
        'apps-ecommerce-product.html',
        products=products
    )


# ================= READ (SINGLE) =================
@products.route('/ecommerce/product/<int:id>')
@login_required
def product_details(id):
    product = Product.query.get_or_404(id)
    return render_template(
        'apps-ecommerce-product_details.html',
        product=product
    )


# ================= UPDATE =================
@products.route('/ecommerce/product/update/<int:id>', methods=['POST'])
@login_required
def update_product(id):
    product = Product.query.get_or_404(id)

    product.title = request.form.get('title')
    product.description = request.form.get('description')
    product.price = request.form.get('price')
    product.stock = request.form.get('stock')
    product.discount = request.form.get('discount')
    product.category = request.form.get('category')
    product.status = request.form.get('status')
    product.visibility = request.form.get('visibility')

    db.session.commit()
    flash("Product updated successfully", "success")
    return redirect(url_for('products.product_list'))


# ================= DELETE =================
@products.route('/ecommerce/product/delete/<int:id>')
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully", "danger")
    return redirect(url_for('products.product_list'))
