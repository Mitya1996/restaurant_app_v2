import os
import datetime
import requests

from flask import Flask, render_template, request, redirect, flash, session, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from models import User, Restaurant

from google.cloud import storage

from gcs_credentials import credentials

from gcs_functions import image_urls, delete_blob

import uuid #for uploading images, random name

from forms import LoginForm, ChangeMenuForm, NewUserForm, AddImageForm, WhatsappPhoneForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')
GOOGLE_STORAGE_BUCKET = os.environ.get('GOOGLE_STORAGE_BUCKET', 'restaurant-app-314718-public')

client = storage.Client(credentials=credentials)

#variable for /images route
UPLOAD_FOLDER = './user-uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#flask-login stuff 
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(username):
    return User.get(username)

#puts restaurant variable in all templates so you can use restaurant.whatsapp_phone and restaurant.menu
@app.context_processor
def inject_user():
    return dict(restaurant=Restaurant())


@app.route('/')
def home():
    user_image_urls = image_urls(GOOGLE_STORAGE_BUCKET, 'user-images/img')
    return render_template('index.html', user_image_urls=user_image_urls)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if '_user_id' in session:
        flash('Ya estas autenticado')
        return redirect('/user')
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if not user:
            flash("Credenciales invalidos")
            return redirect('/login')
            
        # user should be an instance of your `User` class
        login_user(user)

        flash('Entraste la cuenta con exito')

        return redirect('/dashboard')

    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def user():
    menu_form = ChangeMenuForm(obj=Restaurant())

    if menu_form.validate_on_submit():

        user_input = request.form['menu']
        Restaurant.set_menu(user_input)
        flash('menu edited successfully')

        return redirect('/dashboard')

    return render_template('dashboard.html', menu_form=menu_form)


@app.route('/images', methods=['GET', 'POST'])
@login_required
def images():
    #used prefix of img because there is always one hidden blob in buckets, not sure why
    blobs = client.list_blobs(GOOGLE_STORAGE_BUCKET, prefix='user-images/img')

    add_image_form = AddImageForm()
    if add_image_form.validate_on_submit():
        if add_image_form.photo_file.data:
            f = request.files['photo_file']
            import re
            extension = re.findall("(jpg|jpeg|png|gif|bmp)", f.filename)[0]
            filename = f'img-{uuid.uuid4()}.{extension}'
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            photo_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            policy = client.generate_signed_post_policy_v4(
                GOOGLE_STORAGE_BUCKET,
                f'user-images/{filename}',
                expiration=datetime.timedelta(minutes=10),
                conditions=[
                    ["content-length-range", 0, 1000000]
                ],
            )
            with open(photo_url, "rb") as f:
                files = {"file": (photo_url, f)}
                requests.post(policy["url"], data=policy["fields"], files=files)

            return redirect('/images')


    return render_template('images.html', blobs=blobs, add_image_form=add_image_form)


@app.route('/<bucket_name>/user-images/<blob_name>/delete')
@login_required
def delete(bucket_name, blob_name):
    delete_blob(bucket_name, f'user-images/{blob_name}')
    return redirect('/images')


@app.route('/edit-whatsapp-number', methods=['GET', 'POST'])
@login_required
def edit_wa_num():
    #obj parameter is used to prepopulate values in form
    #in this case Restaurant() object has property whatsapp_phone to pull value from
    form = WhatsappPhoneForm(obj=Restaurant())

    if form.validate_on_submit():
        updated_whatsapp_phone = form.whatsapp_phone.data
        Restaurant.set_whatsapp_phone(updated_whatsapp_phone)
        flash('Numero de WhatsApp actualizado')
        return redirect('/settings')

    return render_template('edit-wa-num.html', form=form)


@app.route('/users')
@login_required
def users():
    if not current_user.is_admin:
        flash('No esta permitido gestionar usuarios')
        return redirect('/')
    users = User.get_all()
    return render_template('users.html', users=users)

@app.route('/users/create', methods=['GET', 'POST'])
@login_required
def register():
    if not current_user.is_admin:
        flash('No esta permitido crear usuarios')
        return redirect('/')
    form = NewUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        is_admin = form.is_admin.data
        User.register(username, password, email, is_admin)
        flash('Usuario creado')
        return redirect('/users')
        
    return render_template('create-user.html', form=form)


@app.route('/<username>/delete')
@login_required
def delete_user(username):
    #edge case if a user deletes themselves
    if username == current_user.username:
        flash('No se puede eliminar se mismo')
        return redirect('/users')
    #edge case if a user deletes themselves
    if not current_user.is_admin:
        flash('No esta permitido eliminar usuarios')
        return redirect('/')
    deleted = User.delete(username)
    if deleted:
        flash('Usuario eliminado')
    return redirect('/users')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Saliste de la cuenta')
    return redirect('/')

@app.route("/resetpassword", methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    return render_template('reset-password.html', form=form)
