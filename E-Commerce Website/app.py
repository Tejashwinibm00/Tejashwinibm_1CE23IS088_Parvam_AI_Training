from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Category, Product, Order, OrderItem
import os

BASE_DIR = os.path.dirname(__file__)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'store.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-secret-change-me'

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.context_processor
def inject_categories():
    # provide categories to all templates so base.html can render nav
    try:
        cats = Category.query.all()
    except Exception:
        cats = []
    return dict(categories=cats)


def get_cart():
    return session.setdefault('cart', {})


@app.route('/')
@login_required
def index():
    categories = Category.query.all()
    featured = Product.query.limit(8).all()
    return render_template('index.html', categories=categories, featured=featured)


@app.route('/category/<int:cid>')
@login_required
def category_page(cid):
    cat = Category.query.get_or_404(cid)
    query = Product.query.filter_by(category_id=cid)
    
    # Handle filters
    price_range = request.args.get('price')
    if price_range == 'under50':
        query = query.filter(Product.price < 50)
    elif price_range == '50to200':
        query = query.filter(Product.price >= 50, Product.price <= 200)
    elif price_range == 'over200':
        query = query.filter(Product.price > 200)
        
    brand = request.args.get('brand')
    if brand:
        query = query.filter(Product.name.ilike(f"%{brand}%"))
        
    products = query.all()
    return render_template('category.html', category=cat, products=products)


@app.route('/product/<int:pid>')
def product_page(pid):
    p = Product.query.get_or_404(pid)
    return render_template('product.html', product=p)


@app.route('/search')
def search():
    q = request.args.get('q', '')
    results = []
    if q:
        results = Product.query.filter(Product.name.ilike(f"%{q}%") | Product.description.ilike(f"%{q}%")).all()
    return render_template('search.html', q=q, results=results)


@app.route('/cart')
def cart_page():
    cart = get_cart()
    items = []
    total = 0.0
    for pid, qty in cart.items():
        prod = Product.query.get(int(pid))
        if not prod:
            continue
        item_total = prod.price * qty
        total += item_total
        items.append({'product': prod, 'qty': qty, 'item_total': item_total})
    return render_template('cart.html', items=items, total=total)


@app.route('/cart/add/<int:pid>', methods=['POST'])
def add_to_cart(pid):
    qty = int(request.form.get('qty', 1))
    cart = get_cart()
    cart[str(pid)] = cart.get(str(pid), 0) + qty
    session['cart'] = cart
    flash('Added to cart')
    return redirect(request.referrer or url_for('index'))


@app.route('/cart/update', methods=['POST'])
def update_cart():
    cart = get_cart()
    for pid, qty in request.form.items():
        if not pid.startswith('qty_'):
            continue
        _id = pid.split('_', 1)[1]
        try:
            q = int(qty)
        except ValueError:
            q = 0
        if q <= 0:
            cart.pop(_id, None)
        else:
            cart[_id] = q
    session['cart'] = cart
    return redirect(url_for('cart_page'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart = get_cart()
    if request.method == 'POST':
        # create order
        if not cart:
            flash('Cart empty')
            return redirect(url_for('cart_page'))
        name = request.form.get('name')
        address = request.form.get('address')
        order = Order(customer_name=name, address=address)
        db.session.add(order)
        db.session.flush()
        total = 0.0
        for pid, qty in cart.items():
            prod = Product.query.get(int(pid))
            if not prod:
                continue
            oi = OrderItem(order_id=order.id, product_id=prod.id, quantity=qty, unit_price=prod.price)
            db.session.add(oi)
            total += prod.price * qty
        order.total_amount = total
        db.session.commit()
        session['cart'] = {}
        return render_template('order_confirm.html', order=order)
    # GET
    items = []
    total = 0.0
    for pid, qty in cart.items():
        prod = Product.query.get(int(pid))
        if not prod:
            continue
        items.append({'product': prod, 'qty': qty, 'item_total': prod.price * qty})
        total += prod.price * qty
    return render_template('checkout.html', items=items, total=total)


@app.route('/shipping', methods=['GET', 'POST'])
@login_required
def shipping():
    if request.method == 'POST':
        session['shipping_address'] = request.form.get('address')
        return redirect(url_for('payment'))
    return render_template('shipping.html')


@app.route('/payment', methods=['GET', 'POST'])
@login_required
def payment():
    if request.method == 'POST':
        return redirect(url_for('checkout'))
    return render_template('payment.html')


@app.route('/orders')
@login_required
def order_history():
    orders = Order.query.filter_by(customer_name=current_user.email).all()
    return render_template('orders.html', orders=orders)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@app.route('/support')
def support():
    return render_template('support.html')


@app.route('/shipping-info')
def shipping_info():
    return render_template('shipping_info.html')


@app.route('/returns')
def returns():
    return render_template('returns.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, pwd):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid credentials')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['password']
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))
        u = User(email=email, password_hash=generate_password_hash(pwd))
        db.session.add(u)
        db.session.commit()
        login_user(u)
        return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/security')
@login_required
def security():
    return render_template('security.html')


@app.route('/addresses')
@login_required
def addresses():
    return render_template('addresses.html')


@app.route('/payment-settings')
@login_required
def payment_settings():
    return render_template('payment_settings.html')


@app.route('/admin')
@login_required
def admin_index():
    if not current_user.is_admin:
        flash('Admin only')
        return redirect(url_for('index'))
    products = Product.query.all()
    return render_template('admin/index.html', products=products)


@app.route('/admin/product/new', methods=['GET', 'POST'])
@login_required
def admin_product_new():
    if not current_user.is_admin:
        flash('Admin only')
        return redirect(url_for('index'))
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        category_id = int(request.form['category_id'])
        p = Product(name=name, description=request.form.get('description',''), price=price, category_id=category_id)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('admin_index'))
    cats = Category.query.all()
    return render_template('admin/product_form.html', categories=cats)


if __name__ == '__main__':
    app.run(debug=True)
