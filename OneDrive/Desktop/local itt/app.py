import os
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from config import Config
from models import db, User, Product, Category, CartItem, Order, OrderItem, Supplier, FavoriteProduct, Notification, ChatMessage
from sqlalchemy import func
from rapidfuzz import process, fuzz
import re

app = Flask(__name__)
app.config.from_object(Config)
Config.init_app(app)

# 🚀 SECURE ABSOLUTE MOUNT: Enforcing target media parameters trajectory matrix
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads')

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_customer'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_cart_count():
    if current_user.is_authenticated and current_user.role == 'customer':
        count = sum(item.quantity for item in current_user.cart_items)
        return dict(cart_count=count)
    return dict(cart_count=0)

# 🗺️ IN: Optimized Indian Context Search Mapping
INDIAN_SYNONYM_MATRIX = {
    "seb": "apple", "aloo": "potato", "aalo": "potato", "tamatar": "tomato",
    "pyaaz": "onion", "kela": "banana", "doodh": "milk", "dudh": "milk",
    "dahi": "curd", "atta": "flour", "chawal": "rice", "taza": "fresh"
}

def seed_initial_data():
    if User.query.filter_by(role='admin').first() is None:
        # 🏢 Merchant Hub Outlet Node 1 (Pincode: 713206)
        merchant_1 = User(
            name="Aman Gupta",
            email="merchant1@grocery.com",
            password_hash=generate_password_hash("admin123"),
            phone="9876543210",
            address="Station Road Market Hub, Sector 3",
            role="admin",
            store_name="Gupta Supermart & Kirana",
            pincode="713206"
        )
        # 🏢 Merchant Hub Outlet Node 2 (Pincode: 713216)
        merchant_2 = User(
            name="Vikram Singh",
            email="merchant2@grocery.com",
            password_hash=generate_password_hash("admin123"),
            phone="8765432109",
            address="City Center Commercial Plaza, Ground Floor",
            role="admin",
            store_name="Express O2O Quick Store",
            pincode="713216"
        )
        db.session.add(merchant_1)
        db.session.add(merchant_2)
        db.session.commit()

        cats = [
            Category(name="Fruits"), Category(name="Vegetables"), Category(name="Dairy"),
            Category(name="Snacks"), Category(name="Beverages"), Category(name="Bakery")
        ]
        for c in cats:
            db.session.add(c)
            
        supplier = Supplier(
            name="Local Fresh Wholesale Distributor",
            contact_name="Rajesh Kumar",
            email="rajesh@localfarms.com",
            phone="9876543211"
        )
        db.session.add(supplier)
        db.session.commit()

        # Products mapped securely under strict store isolated nodes
        p1 = Product(name="Fresh Apples (Seb)", sku="FRT-APP-01", brand="Fresh Orchard",
                     description="Crisp apples.", cost_price=80.0, selling_price=120.0, stock_quantity=150, min_stock_level=15,
                     category_id=1, supplier_id=1, store_owner_id=merchant_1.id)
                     
        p2 = Product(name="Taza Whole Milk (1 Litre)", sku="DRY-MLK-02", brand="Taza Dairy",
                     description="Pasteurized milk.", cost_price=50.0, selling_price=60.0, stock_quantity=49, min_stock_level=10,
                     category_id=3, supplier_id=1, store_owner_id=merchant_1.id)
                     
        p3 = Product(name="Fresh White Sliced Bread", sku="BAK-BRD-03", brand="BakeHouse",
                     description="Soft sliced white bread.", cost_price=30.0, selling_price=45.0, stock_quantity=39,
                     min_stock_level=8, category_id=6, supplier_id=1, store_owner_id=merchant_2.id)
                     
        db.session.add_all([p1, p2, p3])
        db.session.commit()

@app.route('/')
def index():
    if current_user.is_authenticated and current_user.role == 'customer':
        local_stores = User.query.filter_by(role='admin', pincode=current_user.pincode).all()
        return render_template('index.html', local_stores=local_stores, browsing_pincode=current_user.pincode)
    all_stores = User.query.filter_by(role='admin').all()
    return render_template('index.html', local_stores=all_stores, browsing_pincode=None)

@app.route('/customer/modify_address', methods=['POST'])
@login_required
def modify_address():
    if current_user.role != 'customer':
        return redirect(url_for('index'))
    new_pincode = request.form.get('pincode', "").strip()
    new_address = request.form.get('address', "").strip()
    if new_pincode and new_address:
        current_user.pincode = new_pincode
        current_user.address = new_address
        db.session.commit()
        flash(f"Location modified to: {new_pincode}", "success")
    return redirect(url_for('index'))
@app.route('/store/<int:store_id>')
@login_required
def view_store_catalog(store_id):
    store = User.query.get_or_404(store_id)
    search_query = request.args.get('search', '').strip()
    cat_id = request.args.get('category_id', type=int)

    # Base query filters matrix matching store configuration
    product_query = Product.query.filter_by(store_owner_id=store_id)

    if search_query:
        # Lowercase clean string parsing
        lower_query = search_query.lower().strip()

        # 🎯 STEP 1: Enhanced Desi Local Terms Map Checklist (Catching spelling variants)
        if lower_query in ["aloo", "alu", "alloo", "aalo", "batata"]:
            search_query = "potato"
        elif lower_query in ["tamatar", "tomatr"]:
            search_query = "tomato"
        elif lower_query in ["seb", "sew"]:
            search_query = "apple"
        elif lower_query in ["doodh", "dudh", "dud"]:
            search_query = "milk"
        elif lower_query in ["pyaz", "pyaaz", "kanda"]:
            search_query = "onion"
        else:
            # 🍫 STEP 2: Fallback to Nonsense Processing if no desi term matched
            clean_query = re.sub(r'[^a-zA-Z\s]', '', search_query).strip()
            has_alphabets = any(c.isalpha() for c in clean_query)
            
            if has_alphabets and len(clean_query) >= 3:
                vowel_check = any(vowel in clean_query.lower() for vowel in ['a', 'e', 'i', 'o', 'u', 'y'])
                if not vowel_check:
                    print(f"--- [NONSENSE SEARCH ENCOUNTERED] ---")
                    search_query = "chocolate"

        # 🚀 STEP 3: Flexible Database Query Context Matching
        # Hum check karenge ki product name, brand ya description mein search_query ho
        product_query = product_query.filter(
            (Product.name.ilike(f'%{search_query}%')) |
            (Product.brand.ilike(f'%{search_query}%')) |
            (Product.description.ilike(f'%{search_query}%'))
        )

    if cat_id:
        product_query = product_query.filter_by(category_id=cat_id)

    products = product_query.all()
    categories = Category.query.all()

    # Dynamic protection matrix flag check
    contains_restricted_items = (cat_id == 5) or any(p.category_id == 5 for p in products)

    # 🔬 Diagnostic Logging in your VS Code terminal
    print(f"🔍 [SEARCH OVERRIDE LOG] Final Query sent to Neon: '{search_query}'")
    print(f"📦 Total matching products fetched: {len(products)}")

    return render_template(
        'store_catalog.html', 
        store=store, 
        products=products, 
        categories=categories, 
        selected_category=cat_id, 
        search_query=search_query,
        contains_restricted_items=contains_restricted_items
    )
    
@app.route('/register/customer', methods=['GET', 'POST'])
def register_customer():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    from forms import CustomerRegistrationForm
    form = CustomerRegistrationForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user = User(name=form.name.data, email=form.email.data, password_hash=hashed_pw,
                    phone=form.phone.data, address=form.address.data, pincode=form.pincode.data, role='customer')
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login_customer'))
    return render_template('register_customer.html', form=form)

@app.route('/login/customer', methods=['GET', 'POST'])
def login_customer():
    if current_user.is_authenticated and current_user.role == 'customer':
        return redirect(url_for('customer_dashboard'))
    from forms import LoginForm
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data, role='customer').first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        flash('Login failed. Please check your inputs.', 'danger')
    return render_template('login_customer.html', form=form)

@app.route('/login/business', methods=['GET', 'POST'])
def login_business():
    if current_user.is_authenticated:
        if current_user.role != 'customer':
            return redirect(url_for('business_dashboard'))
        return redirect(url_for('index'))
    from forms import LoginForm
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.role in ['admin', 'manager', 'cashier', 'staff'] and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash(f"Welcome back to Enterprise Hub: {user.store_name if user.store_name else 'Store Counter'}", "success")
            return redirect(url_for('business_dashboard'))
        else:
            flash('Access Denied. Invalid credentials or unauthorized management personnel record.', 'danger')
    return render_template('login_business.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.route('/customer/dashboard')
@login_required
def customer_dashboard():
    if current_user.role != 'customer':
        return redirect(url_for('index'))
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.order_date.desc()).all()
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    return render_template('customer_dashboard.html', orders=orders, notifications=notifications)

@app.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    active_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if active_items:
        first_product = Product.query.get(active_items[0].product_id)
        if first_product and first_product.store_owner_id != product.store_owner_id:
            flash('Cross-store validation constraint: Cannot mix items from separate stores.', 'danger')
            return redirect(url_for('cart'))
            
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product.id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(user_id=current_user.id, product_id=product.id, quantity=1)
        db.session.add(cart_item)
    db.session.commit()
    return redirect(url_for('cart'))

@app.route('/cart')
@login_required
def cart():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    subtotal = sum(item.product.selling_price * item.quantity for item in items)
    tax = subtotal * 0.05
    return render_template('cart.html', items=items, subtotal=subtotal, tax=tax, total=subtotal+tax)

@app.route('/cart/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_cart_item(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id == current_user.id:
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not items:
        flash('Your shopping cart is empty!', 'warning')
        return redirect(url_for('index'))
    subtotal = sum(item.product.selling_price * item.quantity for item in items)
    tax = subtotal * 0.05
    from forms import CheckoutForm
    form = CheckoutForm()
    if form.validate_on_submit():
        first_prod = Product.query.get(items[0].product_id)
        order = Order(
            user_id=current_user.id, pickup_date=form.pickup_date.data,
            pickup_time_slot=form.pickup_time_slot.data, total_amount=subtotal+tax,
            tax_amount=tax, notes=form.notes.data, status='Pending', store_owner_id=first_prod.store_owner_id
        )
        db.session.add(order)
        db.session.flush()
        
        for item in items:
            item.product.stock_quantity -= item.quantity
            db.session.add(OrderItem(order_id=order.id, product_id=item.product_id, quantity=item.quantity, unit_price=item.product.selling_price))
            
            if item.product.stock_quantity <= item.product.min_stock_level:
                admin_users = User.query.filter(User.role != 'customer').all()
                for admin in admin_users:
                    db.session.add(Notification(user_id=admin.id, title="Low Stock Warning", message=f"Product '{item.product.name}' has dropped below safe limits."))
            db.session.delete(item)
            
        db.session.add(Notification(user_id=current_user.id, title="Order Placed Successfully", message=f"Your pickup order #{order.id} has been submitted to the counter."))
        db.session.commit()
        flash('Your order has been reserved!', 'success')
        return redirect(url_for('customer_dashboard'))
    return render_template('checkout.html', form=form, items=items, total=subtotal+tax)

@app.route('/business/dashboard')
@login_required
def business_dashboard():
    if current_user.role == 'customer':
        return redirect(url_for('index'))
    revenue = db.session.query(func.sum(Order.total_amount)).filter(Order.status == 'Completed', Order.store_owner_id == current_user.id).scalar() or 0.0
    orders_count = Order.query.filter_by(store_owner_id=current_user.id).count()
    low_stock_count = Product.query.filter(Product.stock_quantity <= Product.min_stock_level, Product.store_owner_id == current_user.id).count()
    cust_count = User.query.filter_by(role='customer').count()
    orders = Order.query.filter_by(store_owner_id=current_user.id).order_by(Order.order_date.desc()).all()
    products = Product.query.filter_by(store_owner_id=current_user.id).all()
    categories = Category.query.all()
    return render_template('business_dashboard.html', revenue=revenue, orders_count=orders_count, low_stock_count=low_stock_count, cust_count=cust_count, orders=orders, products=products, categories=categories)

@app.route('/business/order/update/<int:order_id>/<string:new_status>', methods=['POST'])
@login_required
def update_order_status(order_id, new_status):
    order = Order.query.filter_by(id=order_id, store_owner_id=current_user.id).first_or_404()
    order.status = new_status
    friendly_status = "Accepted" if new_status == 'Confirmed' else "Packing" if new_status == 'Preparing' else "Ready for Collection"
    db.session.add(Notification(user_id=order.user_id, title=f"Order Status: {friendly_status}", message=f"Your store pickup order #{order.id} is now '{friendly_status}'."))
    db.session.commit()
    return redirect(url_for('business_dashboard'))

@app.route('/business/product/update-inline/<int:product_id>', methods=['POST'])
@login_required
def update_product_inline(product_id):
    product = Product.query.filter_by(id=product_id, store_owner_id=current_user.id).first_or_404()
    data = request.get_json()
    if 'price' in data: product.selling_price = float(data['price'])
    if 'stock' in data: product.stock_quantity = int(data['stock'])
    db.session.commit()
    return jsonify({"success": True})

@app.route('/business/invoice/<int:order_id>')
@login_required
def view_invoice(order_id):
    order = Order.query.filter_by(id=order_id, store_owner_id=current_user.id).first_or_404()
    return render_template('invoice_print.html', order=order)

@app.route('/business/product/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.filter_by(id=product_id, store_owner_id=current_user.id).first_or_404()
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('business_dashboard'))

@app.route('/business/analytics')
@login_required
def business_analytics():
    if current_user.role == 'customer':
        return redirect(url_for('index'))
    completed_orders = Order.query.filter_by(status='Completed', store_owner_id=current_user.id).all()
    revenue = sum(o.total_amount for o in completed_orders)
    tax = sum(o.tax_amount for o in completed_orders)
    status_counts = {
        'Pending': Order.query.filter_by(status='Pending', store_owner_id=current_user.id).count(),
        'Confirmed': Order.query.filter_by(status='Confirmed', store_owner_id=current_user.id).count(),
        'Preparing': Order.query.filter_by(status='Preparing', store_owner_id=current_user.id).count(),
        'Ready': Order.query.filter_by(status='Ready for Pickup', store_owner_id=current_user.id).count(),
        'Completed': Order.query.filter_by(status='Completed', store_owner_id=current_user.id).count()
    }
    return render_template('analytics.html', revenue=revenue, tax=tax, profit=revenue*0.25, order_count=len(completed_orders), cat_labels=[], cat_sales=[], status_counts=status_counts)

@app.route('/customer/order/cancel/<int:order_id>', methods=['POST'])
@login_required
def cancel_order_customer(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    if order.status != 'Pending':
        flash("Order is already being processed and cannot be cancelled online.", "danger")
        return redirect(url_for('customer_dashboard'))
    for item in order.items:
        item.product.stock_quantity += item.quantity
    order.status = 'Cancelled'
    db.session.commit()
    flash(f"Order #FC-00{order.id} has been successfully cancelled.", "success")
    return redirect(url_for('customer_dashboard'))

@app.route('/favorite/toggle/<int:product_id>', methods=['POST'])
@login_required
def toggle_favorite(product_id):
    if current_user.role != 'customer':
        return redirect(url_for('index'))
    fav = FavoriteProduct.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if fav:
        db.session.delete(fav)
        msg = "Removed from your choice list."
    else:
        fav = FavoriteProduct(user_id=current_user.id, product_id=product_id)
        db.session.add(fav)
        msg = "Added to your choice list!"
    db.session.commit()
    flash(msg, 'info')
    return redirect(request.referrer or url_for('index'))

@app.route('/business/category/add', methods=['POST'])
@login_required
def add_category_backend():
    if current_user.role == 'customer':
        return redirect(url_for('index'))
    cat_name = request.form.get('category_name', "").strip()
    if cat_name:
        existing_cat = Category.query.filter_by(name=cat_name).first()
        if existing_cat:
            flash("That category already exists!", "warning")
        else:
            new_cat = Category(name=cat_name)
            db.session.add(new_cat)
            db.session.commit()
            flash(f"New category '{cat_name}' added successfully!", "success")
    else:
        flash("Category name cannot be blank.", "danger")
    return redirect(url_for('business_dashboard'))

@app.route('/business/product/add', methods=['POST'])
@login_required
def add_product_backend():
    if current_user.role == 'customer':
        return redirect(url_for('index'))
    image_file = request.files.get('product_image')
    filename = 'default_product.jpg'
    if image_file and image_file.filename != "":
        filename = secure_filename(image_file.filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(upload_path)
        
    new_prod = Product(
        name=request.form.get('name'),
        sku=request.form.get('sku'),
        brand=request.form.get('brand'),
        description=request.form.get('description'),
        cost_price=float(request.form.get('cost_price', 0)),
        selling_price=float(request.form.get('selling_price', 0)),
        stock_quantity=int(request.form.get('stock_quantity', 0)),
        min_stock_level=int(request.form.get('min_stock_level', 5)),
        category_id=int(request.form.get('category_id', 1)),
        store_owner_id=current_user.id,
        image_url=filename
    )
    db.session.add(new_prod)
    db.session.commit()
    flash(f"Product '{new_prod.name}' added successfully with its assets!", "success")
    return redirect(url_for('business_dashboard'))

@app.route('/register/business', methods=['GET', 'POST'])
def register_business():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        name = request.form.get('name', "").strip()
        email = request.form.get('email', "").strip()
        phone = request.form.get('phone', "").strip()
        password = request.form.get('password', "").strip()
        store_name = request.form.get('store_name', "").strip()
        pincode = request.form.get('pincode', "").strip()
        address = request.form.get('address', "").strip()
        
        if not all([name, email, phone, password, store_name, pincode, address]):
            flash('All validation profile entry parameters are mandatory!', 'danger')
            return render_template('register_business.html')
            
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('This business communication route is already registered.', 'warning')
            return render_template('register_business.html')
            
        hashed_pw = generate_password_hash(password)
        new_merchant = User(
            name=name, email=email, password_hash=hashed_pw,
            phone=phone, address=address, role='admin',
            store_name=store_name, pincode=pincode
        )
        db.session.add(new_merchant)
        db.session.commit()
        flash(f"Store '{store_name}' registered successfully! Log in to access your Enterprise Hub.", 'success')
        return redirect(url_for('login_business'))
    return render_template('register_business.html')

@app.route('/product/compare/<int:product_id>')
@login_required
def compare_prices(product_id):
    if current_user.role != 'customer':
        return redirect(url_for('business_dashboard'))
    target_product = db.session.get(Product, product_id)
    if not target_product:
        flash("Product configuration record missing.", "danger")
        return redirect(url_for('index'))
        
    target_name_lower = target_product.name.lower().strip()
    target_words = set([w.strip() for w in target_name_lower.split() if len(w) > 2])
    stop_words = {'fresh', 'premium', 'good', 'best', 'organic', 'local', 'quality', 'with', 'and', 'for'}
    clean_target_words = target_words - stop_words
    
    if not clean_target_words:
        clean_target_words = target_words if target_words else {target_name_lower}
        
    synonyms = {
        'banana': ['banana', 'kela', 'kele', 'kelaa'],
        'kela': ['banana', 'kela', 'kele', 'kelaa'],
        'apple': ['apple', 'seb', 'sew'],
        'seb': ['apple', 'seb', 'sew'],
        'milk': ['milk', 'doodh', 'dudh', 'dairy'],
        'doodh': ['milk', 'doodh', 'dudh', 'dairy'],
        'potato': ['potato', 'aloo', 'alu'],
        'aloo': ['potato', 'aloo', 'alu'],
        'onion': ['onion', 'pyaz', 'pyaaz'],
        'pyaz': ['onion', 'pyaz', 'pyaaz'],
        'tomato': ['tomato', 'tamatar'],
        'tamatar': ['tomato', 'tamatar']
    }
    
    search_terms = set()
    for word in clean_target_words:
        search_terms.add(word)
        if word in synonyms:
            search_terms.update(synonyms[word])
            
    query_filters = []
    for term in search_terms:
        query_filters.append(Product.name.ilike(f'%{term}%'))
        query_filters.append(Product.description.ilike(f'%{term}%'))
        
    raw_candidates = db.session.query(Product, User).\
        join(User, Product.store_owner_id == User.id).\
        filter(db.or_(*query_filters), Product.id != product_id).all()
        
    scored_deals = []
    for prod, merchant in raw_candidates:
        prod_name_lower = prod.name.lower()
        prod_words = set(prod_name_lower.split())
        match_score = len(search_terms.intersection(prod_words))
        if match_score > 0:
            scored_deals.append((prod, merchant, match_score))
            
    scored_deals.sort(key=lambda x: (-x[2], x[0].selling_price))
    final_comparison_deals = [(item[0], item[1]) for item in scored_deals]
    return render_template('compare_prices.html', target_product=target_product, comparison_deals=final_comparison_deals)

# 1. Chat window loading route (Customer & Merchant both use this)
@app.route('/chat/<int:chat_user_id>', methods=['GET', 'POST'])
@login_required
def chat_window(chat_user_id):
    # Fetch the recipient context safely
    other_user = User.query.get_or_404(chat_user_id)
    
    if request.method == 'POST':
        msg_text = request.form.get('message_text', '').strip()
        if msg_text:
            new_msg = ChatMessage(
                sender_id=current_user.id,
                receiver_id=chat_user_id,
                message_text=msg_text
            )
            db.session.add(new_msg)
            db.session.commit()
            return redirect(url_for('chat_window', chat_user_id=chat_user_id))

    # Fetch messages exchanged between current user and chat recipient
    messages = ChatMessage.query.filter(
        ((ChatMessage.sender_id == current_user.id) & (ChatMessage.receiver_id == chat_user_id)) |
        ((ChatMessage.sender_id == chat_user_id) & (ChatMessage.receiver_id == current_user.id))
    ).order_by(ChatMessage.timestamp.asc()).all()

    # Debug log terminal checking matrix to verify execution state
    print(f"--- [CHAT WINDOW ROUTE HIT] ---")
    print(f"Current User Name: {current_user.name} | Role: {current_user.role}")
    print(f"Other User Name: {other_user.name} | Role: {other_user.role}")
    print(f"Total Message Rows Found: {len(messages)}")
    print(f"---------------------------------")

    return render_template('chat.html', other_user=other_user, messages=messages)

@app.route('/business/chats')
@login_required
def business_chats_inbox():
    # Structural Guardrail: Customers ko business inbox access karne se roko
    if current_user.role == 'customer':
        return redirect(url_for('index'))
        
    try:
        # 🎯 STEP 1: Find all distinct users who sent a message to this specific merchant
        distinct_senders = db.session.query(ChatMessage.sender_id).\
            filter(ChatMessage.receiver_id == current_user.id).\
            distinct().all()
            
        # 🎯 STEP 2: Find all distinct users to whom this merchant has sent a message
        distinct_receivers = db.session.query(ChatMessage.receiver_id).\
            filter(ChatMessage.sender_id == current_user.id).\
            distinct().all()
            
        # Dono lists ke IDs ko nikal kar ek unique set bana lo
        sender_ids = [s[0] for s in distinct_senders if s[0] is not None]
        receiver_ids = [r[0] for r in distinct_receivers if r[0] is not None]
        all_chat_partner_ids = list(set(sender_ids + receiver_ids))
        
        # 🎯 STEP 3: Fetch full User model profiles for these IDs safely
        active_chats = []
        if all_chat_partner_ids:
            active_chats = User.query.filter(User.id.in_(all_chat_partner_ids)).all()
            
        # Terminal diagnostic debugging logs
        print("--- [MERCHANT INBOX ROUTE HIT] ---")
        print(f"Merchant Logged In: {current_user.name} (ID: {current_user.id})")
        print(f"Unique Chat Partner IDs found: {all_chat_partner_ids}")
        print(f"Total Chat Channels rendered: {len(active_chats)}")
        print("---------------------------------")
        
        return render_template('business_inbox.html', active_chats=active_chats)
        
    except Exception as e:
        print(f"🚨 CRITICAL ERROR inside business_chats_inbox: {str(e)}")
        flash("An error occurred while compiling your chat registry data nodes.", "danger")
        return redirect(url_for('business_dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_initial_data()
    app.run(debug=True, port=5000)