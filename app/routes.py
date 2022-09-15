from app import app,db
from flask import render_template, redirect, url_for, flash
from app.forms import SignUpForm, Cart, LoginForm
from app.models import User, Product, Cart
from flask_login import login_user, logout_user, login_required, current_user
from .forms import Cart


@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
        if existing_user: 
            flash('A user with that username or email already exist.', 'danger')
            return redirect(url_for('signup'))
        new_user = User(email=email, username=username, password=password)
        flash(f"{new_user.username} has been created.", "success")
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)


@app.route('/login', methods = ["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username = username).first()
        if user is not None and user.check_password(password):
            login_user(user)
            flash(f'Welcome back {user.username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Incorrect username and/or password. Please try again', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("You have successfully logged out.", 'primary')
    return redirect(url_for("index"))


@app.route('/myproduct')
@login_required
def my_product():
    products = current_user.products
    total = 0
    for product in products:
        total += int(product.price)
    return render_template('cart.html', products=products, total=total)


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    current_user.products.append(product)
    db.session.commit()
    flash(f"{product.name} was added into your cart", 'warning')
    return render_template('/products', product=product)


@app.route('/product/delete/<int:product_id>', methods=['POST'])
@login_required
def product_delete(product_id):
    product = Product.query.get_or_404(product_id)
    current_user.products.remove(product)
    db.session.commit()
    flash(f"{product.name} has been removed from your cart", 'warning')
    return redirect(url_for('/cart'))


@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/cart')
def cart():
    return render_template('cart.html')