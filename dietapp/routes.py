from dietapp import app
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from dietapp.forms import *
from dietapp.models import *


# Main view
@app.route('/')
@app.route('/home')
@app.route('/products')
@login_required
def products():

    # Creating enabled tabs on layout
    enabled_tabs = create_enabled_tabs()
    enabled_tabs['product'] = False

    # Redirecting admin to his own view
    if current_user.is_admin():
        return redirect(url_for('products_admin'))

    # Rendering view for user with data fetched from database
    return render_template('products.html', title='Produkty', enabled_tabs=enabled_tabs, products=fetch_products())


# Login view
@app.route("/login/", methods=['GET', 'POST'])
def login():

    # Redirecting user to his view if he is logged in
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('products_admin'))
        else:
            return redirect(url_for('products'))

    # Instance of LoginForm
    form = LoginForm()

    # Check that HTTP request is POST and form is valid
    if request.method == 'POST' and form.validate():
        # Check if user exists in database
        user = User.query.filter_by(email=form.username.data).first()

        # Check user credentials and log in
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            # Redirect user to next page if he tried to access user restricted site
            # otherwise redirect to main page
            return redirect(next_page) if next_page else redirect(url_for('login'))
        else:

            # Flash user and return login site
            flash('Nazwa użytkownika lub hasło jest niepoprawne', 'danger')
            return redirect(url_for('login'))

    # Render login view
    return render_template('login.html', form=form, title='Logowanie')


# Register view
@app.route("/register/", methods=['GET', 'POST'])
def register():

    # Redirecting user to his view if he is logged in
    if current_user.is_authenticated:
        return redirect(url_for('products'))

    # Instance of RegisterForm
    form = RegisterForm()

    # Check that HTTP request is POST and form is valid
    if request.method == 'POST' and form.validate_on_submit():
        # Generate hashed password for database
        password_hashed = generate_password_hash(form.password.data, method='sha256')

        # Model object
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            password=password_hashed
        )

        # Save object to database
        db.session.add(new_user)
        db.session.commit()

        flash("Zarejestrowano pomyślnie!", 'success')
        # Redirect to login page
        return redirect(url_for('login'))
    else:
        # Render register site
        return render_template('register.html', form=form, title='Rejestracja')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# Diets view
@app.route('/diets', methods=['GET', 'POST'])
@login_required
def diets():

    # If user uses get method render view
    if request.method == 'GET':

        # Creating enabled tabs on layout
        enabled_tabs = create_enabled_tabs()
        enabled_tabs['diet'] = False

        # Render view with data fetched from model
        return render_template('diets.html', title='Diety', enabled_tabs=enabled_tabs, diets=fetch_diets())

    # If user uses post method
    # Get diet id from form
    diet = int(request.form.get('diet'))

    # If new diet id is different from current one change it in database and flash user with success massage
    if diet and diet != current_user.diet_id:
        current_user.diet_id = diet
        db.session.commit()
        flash('Pomyślnie zmieniono dietę', 'success')
    return redirect(url_for('diets'))


# Meals view
@app.route('/meals', methods=['GET'])
@login_required
def meals():
    enabled_tabs = create_enabled_tabs()
    enabled_tabs['meal'] = False
    return render_template('meals.html', title='Posiłki', enabled_tabs=enabled_tabs)


# Statistics view
@app.route('/statistics', methods=['GET'])
@login_required
def statistics():
    enabled_tabs = create_enabled_tabs()
    enabled_tabs['stats'] = False
    return render_template('statistics.html', title='Statystyki', enabled_tabs=enabled_tabs)


# Admin_products view
@app.route('/products_admin', methods=['GET'])
@login_required
def products_admin():

    # If user is an admin render admin_product view with data fetched from database
    if current_user.is_admin():
        return render_template('admin_templates/products_admin.html',
                               title='Zarządzanie produktami',
                               products=fetch_products())

    # If user tries to get to admin view redirect request to users view
    else:
        return redirect(url_for('products'))


# Admin_products_add view
@app.route('/products_admin/add', methods=['GET', 'POST'])
@login_required
def products_admin_add():

    # Instance of products form
    form = ProductForm()

    # If request method is get render view with form
    # If user tries to load this view redirect user to product view
    if request.method == 'GET':
        if current_user.is_admin():

            return render_template('admin_templates/products_admin_add.html',
                                   title='Zarządzanie produktami',
                                   form=form)
        else:
            return redirect(url_for('products'))

    # If request method is post and form is validated
    if request.method == 'POST' and form.validate_on_submit():

        # Create product
        product = Product(
            name=form.product_name.data,
            calorie=form.calorie.data,
            carbohydrate=form.carbohydrate.data,
            fat=form.fat.data,
            protein=form.protein.data,
            user_id=current_user.id
        )
        # Add product and commit to database
        db.session.add(product)
        db.session.commit()

        # Flash admin with success massage
        flash('Dodano produkt', 'success')

        # Redirect to admin_product view
        return redirect(url_for('products_admin'))

    # If form failed validation flash user with error messages pointing out errors and render view
    flash_form_errors(form)
    return render_template('admin_templates/products_admin_add.html',
                           title='Zarządzanie produktami',
                           form=form)


def create_enabled_tabs():
    return {
        'product': True,
        'diet': True,
        'meal': True,
        'stats': True
    }


# Parses query result to list
def parse_query(query):
    result = []
    for pr in query:
        result.append(pr.get_dict())
    return result


# Fetches all products from database and returns them as list
def fetch_products():
    return parse_query(Product.query.all())


# Fetches all diets from database and returns them as list
def fetch_diets():
    return parse_query(Diet.query.all())


# Flashes user with errors from form validation
def flash_form_errors(form):
    if form.errors:
        for error_field, error_message_list in form.errors.items():
            for error_message in error_message_list:
                flash(error_message, 'danger')
