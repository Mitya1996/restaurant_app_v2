import os
import datetime
import requests

from flask import Flask, render_template, request, redirect, flash
from flask_login import LoginManager, login_user, login_required

from database import db
from models import User

from google.cloud import storage

from gcs_credentials import credentials

from gcs_functions import image_urls, delete_blob

import uuid #for uploading images, random name

from forms import LoginForm, ChangeMenuForm, NewUserForm, AddImageForm

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


@app.route('/images', methods=['GET', 'POST'])
@login_required
def images():
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


@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    new_user_form = NewUserForm()
    if new_user_form.validate_on_submit():

        new_user = User.register(username, password, email, isAdmin)

        db.collections('users').document(new_user.username).set(new_user.to_dict())


