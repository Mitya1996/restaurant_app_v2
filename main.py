import os

from flask import Flask, render_template, request, redirect

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from google.cloud import storage


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')
CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']


# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': 'restaurant-app-314718',
})

db = firestore.client()


@app.route('/')
def home():
    doc = db.collection('restaurant').document('menu').get()

    if doc.exists:
        menu = doc.to_dict()['text']
    else:
        menu = ''

    return render_template('index.html', menu=menu)


@app.route('/update', methods=['POST'])
def update():
    user_input = request.form['menu-textarea-input']

    updated_menu = {
        'text' : user_input
    }
    db.collection('restaurant').document('menu').set(updated_menu)

    return redirect('/')


