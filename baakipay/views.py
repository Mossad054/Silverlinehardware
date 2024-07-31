import os
from flask import Blueprint, render_template, flash, redirect, request, jsonify, url_for, current_app, send_from_directory
from .models import Product, Cart, Order, OrderItem, Complaint
from flask_login import login_required, current_user
from . import db
from intasend import APIService
from .utils import role_required
from .forms import ComplaintForm

# Initialize the Blueprint
views = Blueprint('views', __name__)

# Set API keys
API_PUBLISHABLE_KEY = 'YOUR_PUBLISHABLE_KEY'
API_TOKEN = 'YOUR_API_TOKEN'

@views.route('/')
def home():
    """Render the home page with paginated products."""
    page = request.args.get('page', 1, type=int)
    items = Product.query.paginate(page=page, per_page=12)
    
    for item in items.items:
        if item.product_picture:
            item.product_picture = url_for('views.serve_media', filename=item.product_picture)
        else:
            item.product_picture = url_for('static', filename='images/default_product_image.jpg')
    
    return render_template('home.html', items=items)

@views.route('/media/<path:filename>')
def serve_media(filename):
    """Serve media files from the media directory."""
    return send_from_directory(os.path.join(current_app.root_path, '..', 'media'), filename)

@views.route('/add-to-cart/<int:item_id>')
@login_required
def add_to_cart(item_id):
    """Add a product to the cart."""
    item_to_add = Product.query.get(item_id)
    if not item_to_add:
        flash('Product not found.')
        return redirect(request.referrer)
    
    item_exists = Cart.query.filter_by(product_link=item_id, customer_link=current_user.id).first()
    if item_exists:
        item_exists.quantity += 1
    else:
        new_cart_item = Cart(quantity=1, product_link=item_to_add.id, customer_link=current_user.id)
        db.session.add(new_cart_item)
    
    try:
        db.session.commit()
        flash(f'{item_to_add.product_name} added to cart')
    except Exception as e:
        db.session.rollback()
        flash('Error adding item to cart. Please try again.')
        current_app.logger.error(f'Error adding item to cart: {str(e)}')

    return redirect(request.referrer)

@views.route('/cart', methods=['GET'])
@login_required
def cart():
    """Display the user's cart with total amount."""
    cart_items = Cart.query.filter_by(customer_link=current_user.id).all()
    amount = sum(item.product.current_price * item.quantity for item in cart_items)
    return render_template('cart.html', cart=cart_items, amount=amount, total=amount + 200)

@views.route('/update-cart', methods=['POST'])
@login_required
def update_cart():
    """Update cart item quantities or remove items."""
    cart_id = request.form.get('cart_id')
    action = request.form.get('action')
    
    cart_item = Cart.query.get(cart_id)
    if not cart_item or cart_item.customer_link != current_user.id:
        return jsonify({'error': 'Invalid cart item'}), 400
    
    if action == 'plus':
        cart_item.quantity += 1
    elif action == 'minus':
        cart_item.quantity = max(0, cart_item.quantity - 1)
    elif action == 'remove':
        db.session.delete(cart_item)
    else:
        return jsonify({'error': 'Invalid action'}), 400
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error updating cart: {str(e)}')
        return jsonify({'error': 'Error updating cart'}), 500
    
    cart = Cart.query.filter_by(customer_link=current_user.id).all()
    amount = sum(item.product.current_price * item.quantity for item in cart)
    
    return jsonify({
        'quantity': cart_item.quantity if action != 'remove' else 0,
        'amount': amount,
        'total': amount + 200
    })

@views.route('/place-order')
@login_required
def place_order():
    """Place an order for the items in the cart."""
    customer_cart = Cart.query.filter_by(customer_link=current_user.id).all()
    if not customer_cart:
        flash('Your cart is empty. Add items to your cart before placing an order.')
        return redirect(url_for('views.cart'))

    try:
        total = sum(item.product.current_price * item.quantity for item in customer_cart)
        new_order = Order(status='placed', total_amount=total, customer_link=current_user.id)
        db.session.add(new_order)
        db.session.flush()

        for cart_item in customer_cart:
            product = cart_item.product
            if product.in_stock < cart_item.quantity:
                db.session.rollback()
                flash(f'Not enough stock for {product.product_name}')
                return redirect(url_for('views.cart'))
            
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=cart_item.product_link,
                quantity=cart_item.quantity,
                price=product.current_price
            )
            db.session.add(order_item)
            product.in_stock -= cart_item.quantity

        # Clear the user's cart
        Cart.query.filter_by(customer_link=current_user.id).delete()

        db.session.commit()
        flash('Your order has been placed successfully.')
        return redirect(url_for('views.orders'))
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error placing order: {str(e)}')
        flash('Error placing order. Please try again.')
        return redirect(url_for('views.cart'))

@views.route('/orders')
@login_required
def orders():
    """Display the user's orders."""
    my_orders = Order.query.filter_by(customer_link=current_user.id).all()
    return render_template('orders.html', orders=my_orders)

@views.route('/payment/<int:order_id>', methods=['GET', 'POST'])
@login_required
def payment(order_id):
    """Handle the payment for an order."""
    order = Order.query.get_or_404(order_id)
    if order.customer_link != current_user.id:
        flash('You do not have permission to access this order.')
        return redirect(url_for('views.orders'))
    
    if request.method == 'POST':
        payment_method = request.form.get('payment_method')
        if payment_method == 'mpesa':
            # TODO: Implement M-Pesa integration
            order.status = 'Paid'
            db.session.commit()
            flash('Payment successful. Thank you for your order!')
            return redirect(url_for('views.orders'))
        else:
            flash('Invalid payment method selected.')
    
    return render_template('payment.html', order=order)

@views.route('/complaint', methods=['GET', 'POST'])
@login_required
@role_required(['Customer'])
def complaint():
    """Submit a complaint."""
    form = ComplaintForm()
    if form.validate_on_submit():
        new_complaint = Complaint(
            subject=form.subject.data,
            message=form.message.data,
            customer_link=current_user.id
        )
        db.session.add(new_complaint)
        db.session.commit()
        flash('Complaint Submitted Successfully')
        return redirect(url_for('views.home'))

    return render_template('complaint.html', form=form)


if __name__ == '__main__':
    views.run(debug=True)   
