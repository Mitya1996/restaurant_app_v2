import os

from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_user, login_required

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from gcs_read_images import image_urls

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')
GOOGLE_STORAGE_BUCKET = os.environ.get('GOOGLE_STORAGE_BUCKET', 'restaurant-app-314718-public')


# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': 'restaurant-app-314718',
})

db = firestore.client()


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.collection('users').document(user_id).get()


@app.route('/')
def home():
    doc = db.collection('restaurant').document('menu').get()

    if doc.exists:
        menu = doc.to_dict()['text']
    else:
        menu = ''

    user_image_urls = image_urls(GOOGLE_STORAGE_BUCKET, 'user-images/img')
    return render_template('index.html', menu=menu, user_image_urls=user_image_urls)


@app.route('/update', methods=['POST'])
def update():
    user_input = request.form['menu-textarea-input']

    updated_menu = {
        'text' : user_input
    }
    db.collection('restaurant').document('menu').set(updated_menu)

    return redirect('/')


