from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Product, Order
from . import db
from .utils import role_required

merchant = Blueprint('merchant', __name__)

@merchant.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'merchant':
        flash('Access denied. Merchant account required.', category='error')
        return redirect(url_for('views.home'))
    
    products = Product.query.filter_by(merchant_id=current_user.id).all()
    orders = Order.query.join(Product).filter(Product.merchant_id == current_user.id).all()
    return render_template('merchant/dashboard.html', products=products, orders=orders)

@merchant.route('/add-product', methods=['GET', 'POST'])
@login_required
def add_product():
    if current_user.role != 'merchant':
        flash('Access denied. Merchant account required.', category='error')
        return redirect(url_for('views.home'))
    
    if request.method == 'POST':
        # Handle product creation
        # ...

        return render_template('merchant/add_product.html')

# Add more merchant-specific routes as needed