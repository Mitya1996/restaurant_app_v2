import os

from flask import Flask, render_template, request, redirect, flash
from flask_login import LoginManager, login_user, login_required

from database import db
from models import User

from gcs_read_images import image_urls

from forms import LoginForm, ChangeMenuForm, NewUserForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')
GOOGLE_STORAGE_BUCKET = os.environ.get('GOOGLE_STORAGE_BUCKET', 'restaurant-app-314718-public')


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(username):
    return User.get(username)


@app.route('/')
def home():
    doc = db.collection('restaurant').document('menu').get()

    if doc.exists:
        menu = doc.to_dict()['text']
    else:
        menu = ''

    user_image_urls = image_urls(GOOGLE_STORAGE_BUCKET, 'user-images/img')
    return render_template('index.html', menu=menu, user_image_urls=user_image_urls)



@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if not user:
            flash("invalid credentials")
            return redirect('/login')
            
        # user should be an instance of your `User` class
        login_user(user)

        flash('Logged in successfully.')

        return redirect('/edit')

    return render_template('login.html', form=form)


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    doc = db.collection('restaurant').document('menu').get()

    if doc.exists:
        menu = doc.to_dict()['text']
    else:
        menu = ''
    menu_form = ChangeMenuForm()
    menu_form.menu.data = menu

    if menu_form.validate_on_submit():
        user_input = request.form['menu']

        updated_menu = {
            'text' : user_input
        }
        db.collection('restaurant').document('menu').set(updated_menu)
        flash('menu edited successfully')
        return redirect('/edit')

    return render_template('edit.html', menu_form=menu_form)



@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    new_user_form = NewUserForm()
    if new_user_form.validate_on_submit():

        new_user = User.register(username, password, email, isAdmin)

        db.collections('users').document(new_user.username).set(new_user.to_dict())


