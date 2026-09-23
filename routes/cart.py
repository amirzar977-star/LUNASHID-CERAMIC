from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from models.product import Product

cart_bp = Blueprint('cart', __name__)


def get_cart():
    return session.get('cart', {})


def save_cart(cart):
    session['cart'] = cart
    session.modified = True


@cart_bp.route('/')
def view_cart():
    cart = get_cart()
    items = []
    total = 0
    for pid, qty in cart.items():
        product = Product.query.get(int(pid))
        if product:
            subtotal = product.final_price * qty
            total += subtotal
            items.append({'product': product, 'qty': qty, 'subtotal': subtotal})
    return render_template('cart.html', items=items, total=total)


@cart_bp.route('/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    cart = get_cart()
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    save_cart(cart)
    flash(f'«{product.name}» به سبد خرید اضافه شد.', 'success')
    return redirect(request.referrer or url_for('shop.shop'))


@cart_bp.route('/remove/<int:product_id>')
def remove_from_cart(product_id):
    cart = get_cart()
    cart.pop(str(product_id), None)
    save_cart(cart)
    return redirect(url_for('cart.view_cart'))


@cart_bp.route('/checkout')
def checkout():
    cart = get_cart()
    if not cart:
        return redirect(url_for('shop.shop'))
    return render_template('checkout.html')