#Google's free firestore database (if you don't use it too much)
import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def GOOGLE_APPLICATION_CREDENTIALS():
    GOOGLE_APPLICATION_CREDENTIALS = 'key.json'
    #set in Cloud Run, a secret from secret manager
    GOOGLE_APPLICATION_CREDENTIALS_TEXT = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_TEXT')

    file = open(GOOGLE_APPLICATION_CREDENTIALS, 'w')
    file.write(GOOGLE_APPLICATION_CREDENTIALS_TEXT)
    file.close()
    return GOOGLE_APPLICATION_CREDENTIALS

cred = credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS())

firebase_admin.initialize_app(cred, {
  'projectId': 'restaurant-app-314718',
})

db = firestore.client()